# -*- coding: utf-8 -*-

from nav_msgs.msg import OccupancyGrid
from visualization_msgs.msg import Marker, MarkerArray
from nav2_dynamic_msgs.msg import Obstacle, ObstacleArray  # TODO: ensure this is properly imported

from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener

from logging import getLogger

_logger = getLogger(__name__)

_variable_start_character = '{'
_variable_end_character = '}'


class DetectionCostmapRule(models.Model):
    _name = "detection.costmap.rule"
    _description = 'Detection costmap generation Rules'

    def __init__(self):
        super().__init__('detection_costmap_rule')
        # TODO: evaluate whether or not to save parameters as class variables
        self.declare_parameters(
            namespace='',
            parameters=[
                # input params
                ('detection_topic', "dynamic_object"),  # remapping is better then using parameters?
                ('sequence', 1),
                # cost calculation params
                ('direction_type', "linear"),
                ('cost_type', "falloff"),
                ('falloff_type', "rel_percentage"),
                ('base_cost', 10),
                ('falloff', 0.5),
                ('min_range', 0),
                ('max_range', 10),
                # custom params?
                ('global_frame', "camera_link"),
                ('process_noise_cov', [2., 2., 0.5]),
                ('top_down', False),
                ('death_threshold', 3),
                ('measurement_noise_cov', [1., 1., 1.]),
                ('error_cov_post', [1., 1., 1., 10., 10., 10.]),
                ('vel_filter', [0.1, 2.0]),
                ('height_filter', [-2.0, 2.0]),
                ('cost_filter', 1.0)
            ])
        self.detection_topic = self.get_parameter("detection_topic")._value
        # TODO: make topic_name dynamic based on param (detection_publisher -> self.detection_topic)
        #  although nav2 cpp costmap takes the topicname as class init input...?
        self.costmap_publisher = self.create_publisher(OccupancyGrid, 'detection_publisher', 10)

        # subscribe to trackers
        self.tracker_sub = self.create_subscription(
            ObstacleArray,
            'tracking',
            self.track_callback,
            10)
        self.marker_sub = self.create_subscription(
            MarkerArray,
            'tracking_marker',
            self.marker_callback,
            10)

        self.detection_list = []
        self.sec = 0
        self.nanosec = 0

        # publisher for costmap  # TODO: implement
        self.tracker_obstacle_pub = self.create_publisher(ObstacleArray, 'detection_costmap', 10)
        self.tracker_marker_pub = self.create_publisher(MarkerArray, 'tracking_marker', 10)

        # setup tf related # TODO: is this needed? what is this?
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        # This enables the ordering of rules. In case the order in which the rules are applied are important (shouldnt)
        self.sequence = self.get_parameter("sequence")._value 
        
        # rule type decides if configuring is done via parameters or code: choices = ['parameters', 'code']
        # Use code if both direction and cost are custom, otherwise use parameters
        self.rule_type = self.get_parameter("rule_type")._value
        # TODO: misnomers?
        """
        direction type decides the direction of the costs: choices = ['vector', 'linear', 'gradient', 'custom']
            vector -> costs are added to one side. 
            linear -> costs are added to each side.
            gradient -> costs are added all around each side. # TODO: is this misnomer?
            TODO # custom -> implement own direction choice via "to_be_decided_function"
        """
        self.direction_type = self.get_parameter("direction_type")._value
        """
        cost type decides the way costs change: choices = ['falloff', 'reverse_falloff', 'custom']
        
        falloff decreases the cost each cell
            Used Params:
                base_cost - cost at origin (in the following examples base_cost = 10 is assumed)
                falloff_type - determines the way falloff is applied. See '_get_falloff_costs' for implementation
                    rel_percentage - percentage from last cell (e.g 10, 5, 2.5, 1.25 for 4 cells with 0.5 falloff)
                    abs_percentage - additive percentage from first cell (e.g 10, 9, 8, 7 for 0-3 cells with 0.1 falloff)
                    linear (unneeded?) - additive from last cell (e.g 10, 9, 8, 7 for 4 cells with 1 falloff) 
                    custom - override "get_custom_falloff_costs" to apply your own falloff type
                falloff (0-1 for *_percentage, x for linear) - determines the costs decrease each cell
                min/max_range determines the start and end of falloff (inclusive) (before min falloff = 0 and after max falloff = 1)
                
        reverse_falloff applies costs from max_range -> min_range instead of min_range->max_range. 
            Practically like setting falloff negative with regular falloff type. However with custom, it enables some different approaches
        
        custom applies your own function. To use, overwrite "get_custom_costs(self, min_range, max_range, cell_size):"
        """
        self.cost_type = self.get_parameter("cost_type")._value
        # TODO: implement
        # TODO: add lambda choice?
        # self.falloff_type = self.get_parameter("falloff_type")._value
        # self.falloff = self.get_parameter("falloff")._value
        # self.max_range = self.get_parameter("max_range")._value
        # self.min_range = self.get_parameter("min_range")._value
        # could we have a boolean to check for current path?
        # intersection_check = fields.Boolean

        # parameters for cell size?
        self.cell_unit = "m"
        self.cell_size = 1
        self.use_cell_size = False

    # should we allow smth like this? Maybe with lambda
    # def clean_string(self, string):
    #     clean_string = string.strip()
    #     clean_string = clean_string.replace(_variable_start_character, '')
    #     clean_string = clean_string.replace(_variable_end_character, '')
    #     return clean_string
    """
    # def eval_string(self, locals_dict, string=False):
    check_string = False
    if string:
        check_string = string
    elif self.formula:
        check_string = self.formula

    if check_string:
        try:
            clean_formula = self.clean_string(check_string)
            value = safe_eval(clean_formula, locals_dict=locals_dict, nocopy=True)
        except Exception:
            value = False
    else:
        value = False

    return value
    """

    def get_custom_falloff_costs(self, obstacle_length, base, falloff):
        """
        Return a list of costs. This list will be handled according to your cost type (reversed for reverse_falloff).
        """
        return NotImplementedError("You have to overwrite get_custom_falloff_costs in order to use 'custom' falloff type")

    def _get_falloff_costs(self, obstacle_length, base, falloff, falloff_type):
        falloff_choices = ['rel_percentage', 'abs_percentage', 'linear', 'custom']
        if falloff_type not in falloff_choices:
            raise IOError(f"Selected falloff type not implemented. Possible choices are {falloff_choices}")
        costs = []
        if falloff_type == 'rel_percentage':
            costs = [base*(falloff**distance) for distance in range(obstacle_length)]
        if falloff_type == 'abs_percentage':
            costs = [base*(1-distance*falloff) for distance in range(obstacle_length)]
        if falloff_type == 'linear':
            costs = [base + distance*falloff for distance in range(obstacle_length)]
        if falloff_type == 'custom':
            costs = self.get_custom_falloff_costs(obstacle_length, base, falloff)
        return costs

    def get_custom_costs(self, min_range, max_range, cell_size=False, falloff="Not input?"):
        return []

    def _get_direction_costs(self, cost_type, min_range, max_range, cell_size, falloff="Not input?"):
        """
        returns a list of costs for a specific direction
        """
        choices = ['falloff', 'reverse_falloff', 'custom']
        if cost_type not in choices:
            raise IOError(f"Selected cost type not implemented. Possible choices are {choices}")
        if cost_type in ['falloff', 'reverse_falloff']:
            if self.use_cell_size:
                # if range in distance
                obstacle_length = (max_range-min_range)/cell_size  # 9-2/ 2 = 3.5 -> 0, 0, 10, 10,
                return NotImplementedError("Using cell_size and distance-based ranges are not yet implemented. \n"
                                           "Please set parameter: 'use_cell_size: False")
            else:
                # if range in costmap cells
                # 9 - 2 = 7 -> 0c0, 0c1, 1c2, 2c3, 3c4, 4c5, 5c6, 6c7, 7c8, 8c9,
                obstacle_length = (max_range-min_range)+1  # since both ranges are inclusive, we need to add 1:
                base_cost = self.get_parameter("base_cost")._value
                falloff = self.get_parameter("falloff")._value
                falloff_type = self.get_parameter("falloff_type")._value
                costs = self._get_falloff_costs(obstacle_length, base_cost, falloff, falloff_type)
                if len(costs) != obstacle_length:
                    raise ValueError("Received different amount of falloff than specified by range.")
                if falloff_type == 'reverse_falloff':
                    return costs.reverse()
                else:
                    return costs
        if cost_type == 'custom':
            return self.get_custom_costs(min_range, max_range, cell_size)

    def get_costmap(self):

        rule_type_choices = ['parameters', 'code']
        direction_type = ['vector', 'linear', 'gradient', 'custom']

        rule_type = self.get_parameter("rule_type")._value
        direction_type = self.get_parameter("direction_type")._value
        cost_type = self.get_parameter("cost_type")._value
        max_range = self.get_parameter("max_range")._value
        min_range = self.get_parameter("min_range")._value

        if rule_type not in rule_type_choices:
            raise IOError(f"Selected rule type not implemented. Possible choices are {rule_type_choices}")

            if direction_type not in direction_type:
                raise IOError(f"Selected direction type not implemented. Possible choices are {direction_type}")





    @api.depends('intersection_check', 'tag_ids', 'attribute_ids')
    def _compute_selectable_products(self):
        for record in self:
            if not record.tag_ids and not record.attribute_ids:
                record.selectable_products = False
                record.default_product = False
                continue
            search_domain = []
            if record.tag_ids:
                search_domain.append(('all_product_tag_ids', 'in', record.tag_ids.ids))
            if record.attribute_ids:
                search_domain.append(('product_template_attribute_value_ids', 'in', record.attribute_ids.ids))
            if search_domain:
                products = self.env['product.product'].search(search_domain)
            else:
                products = False
            if record.intersection_check:
                search_domain = []
                for tag in record.tag_ids:
                    search_domain.append(('all_product_tag_ids', 'in', tag.ids))
                for attribute in record.attribute_ids:
                    search_domain.append(('product_template_attribute_value_ids', 'in', attribute.ids))
                products = self.env['product.product'].search(search_domain)

            record.selectable_products = products
