#include "nav2_plugin_tutorial/tutorial_costmap_plugin.hpp"

#include <string>
#include "nav2_costmap_2d/costmap_math.hpp"
#include "nav2_costmap_2d/footprint.hpp"
#include "rclcpp/parameter_events_filter.hpp"

using nav2_costmap_2d::LETHAL_OBSTACLE;

namespace simple_semantic_costmap{

/*
1) Klassidele saab defineerida reegleid, kuidas selle klassi ümber kulu määrata. (Saab erinevalt käsitleda globaalsel ja lokaalsel kaardil)
1.2) Siinkohal on mõistlik teha ka klasside ümberklassifitseerija ja kõige lihtsam esimene lahendus siis jagab klassid kaheks:
Liikuvad ja staatilised. Ma veel mõtlen ja katsetan, kas vaja ainult liikuvatele siis kiht teha (staatilised on ju vaikimisi teiste kihtide poolt tehtud)
2) Kuulab semantilist infot ja loob siis oma kihi selle põhjal
3) Hoiab infot eelneva kaardi seisundi kohta, ilmselt kaks mitte järjestikust kaadrit
4) Reegel kahe klassi eristamise põhjal kulukaardi kihi tegemiseks. Kui liikumisvõimeline objekt seisab paigal,
siis arvestatakse seda kui natukene suuremat staatilist objekti, kui liigub, siis ennustab, kus ette jääb -
tõenäosusliku jaotusega vastavalt teeb siis kulud trajektoorile.

(Selle jaoks oleks parem panoptiline segmenteerimine, aga ma lahendan selle sisuliselt eeldusega, et objektid liiguvad aeglaselt.
Ja kui mitu liikumisvõimellist objekti on ühes kohas, siis käsitletakse neid esimese põhimõttega (suuremana) paigalseisvana kaardi peal,
niikaua kuni nad üksteisest piisavalt kaugel on.)
*/
// I think these are the bounds of the last updated section of the map?
SimpleSemanticLayer::SimpleSemanticLayer() {}

//Method to call, at the end of initialization.
void SimpleSemanticLayer::onInitialize(){
    auto node = node_.lock();
    if (!node) {
        throw std::runtime_error{"Failed to lock node"};
    }
    declareParameter("enabled", rclcpp::ParameterValue(true)); //  enabled_ = node->declare_parameter(name_ + "." + "enabled", true);
    node->get_parameter(name_ + ".enabled", enabled_);

    // Get the path of the map slice topic.
    //TODO:
    //Nvidia had it's solution via parameters, but we prefer remapping
    std::string simple_semantic_map_slice_topic = "/nvblox_node/static_map_slice";

    //set parameters
    // TODO: implement or remove these according to need
    // TODO: add
    max_obstacle_distance_ = node->declare_parameter<float>(getFullName("max_obstacle_distance"), max_obstacle_distance_);
    inflation_distance_ = node->declare_parameter<float>(getFullName("inflation_distance"), inflation_distance_);
    max_cost_value_ = node->declare_parameter<uint8_t>(getFullName("max_cost_value"), max_cost_value_);

      RCLCPP_INFO_STREAM(
    node->get_logger(),
    "Name: " << name_ << " Topic name: " << nvblox_map_slice_topic <<
      " Max obstacle distance: " << max_obstacle_distance_);

    need_recalculation_ = false;
    current_ = true;
}
void NvbloxCostmapLayer::onInitialize()
{
  auto node = node_.lock();
  if (!node) {
    throw std::runtime_error{"Failed to lock node"};
  }
  enabled_ = node->declare_parameter(name_ + "." + "enabled", true);

  // Get the path of the map slice topic.
  std::string nvblox_map_slice_topic = "/nvblox_node/static_map_slice";

  nvblox_map_slice_topic = node->declare_parameter<std::string>(
    getFullName("nvblox_map_slice_topic"), nvblox_map_slice_topic);
  max_obstacle_distance_ = node->declare_parameter<float>(
    getFullName("max_obstacle_distance"), max_obstacle_distance_);
  inflation_distance_ = node->declare_parameter<float>(
    getFullName("inflation_distance"), inflation_distance_);
  max_cost_value_ = node->declare_parameter<uint8_t>(
    getFullName("max_cost_value"), max_cost_value_);

  RCLCPP_INFO_STREAM(
    node->get_logger(),
    "Name: " << name_ << " Topic name: " << nvblox_map_slice_topic <<
      " Max obstacle distance: " << max_obstacle_distance_);

  // Add subscribers to the nvblox message.
  slice_sub_ = node->create_subscription<nvblox_msgs::msg::DistanceMapSlice>(
    nvblox_map_slice_topic, 1,
    std::bind(
      &NvbloxCostmapLayer::sliceCallback, this,
      std::placeholders::_1));
  current_ = true;
}

// With the example of NVIDIA-ISAAC-ROS
// The method is called to ask the plugin: which area of costmap it needs to
// update.
void SimpleSemanticLayer::updateBounds(
  double /*robot_x*/, double /*robot_y*/,
  double /*robot_yaw*/, double * min_x,
  double * min_y, double * max_x,
  double * max_y)
{
  // We give the full AABB of the map that we have available to the
  // upstream controller.
  // According to nav2 the bounds can only grow bigger. So we only update the
  // bounds if it grows bigger or we keep the old values
  if (slice_ != nullptr) {
    const double current_plugin_min_x = slice_->origin.x;
    const double current_plugin_min_y = slice_->origin.y;
    const double current_plugin_max_x = current_plugin_min_x + slice_->width * slice_->resolution;
    const double current_plugin_max_y = current_plugin_min_y + slice_->height * slice_->resolution;

    if (current_plugin_min_x < *min_x) {
      *min_x = current_plugin_min_x;
    }
    if (current_plugin_max_x > *max_x) {
      *max_x = current_plugin_max_x;
    }
    if (current_plugin_min_y < *min_y) {
      *min_y = current_plugin_min_y;
    }
    if (current_plugin_max_y > *max_y) {
      *max_y = current_plugin_max_y;
    }
  }

  auto node = node_.lock();
  if (!node) {
    throw std::runtime_error{"Failed to lock node"};
  }

  RCLCPP_DEBUG(
    node->get_logger(),
    "Update bounds: Min x: %f Min y: %f Max x: %f Max y: %f", *min_x,
    *min_y, *max_x, *max_y);
}

// what is footprint? currently says we need to recalculate and loggs if this is called.
void TutorialLayer::onFootprintChanged(){
    need_recalculation_ = true;
    // this is useful :)
    RCLCPP_INFO(rclcpp::get_logger(
        "nav2_costmap_2d"), "TutorialLayer::onFootprintChanged() num of footprint points: %lu",
        layered_costmap_->getFootprint().size());
}

// Method to recalculate costmap. Updates with window bounds (defined by 2 coordinates: {min_i, min_j} - {max_i, max_j})
void TutorialLayer::updateCosts(nav2_costmap_2d::Costmap2D & master_grid, int min_i, int min_j, int max_i, int max_j){
    // if our layer is disabled, we do nothing - decided by plugin usage?
    if (!enabled_) {
    return;
    }
/*
    master_grid - final (result) costmap (all layers)
    costmap_ - current layer pointer. use this with any update method:
     - updateWithAddition()
     - updateWithMax()
     - updateWithOverwrite()
     - updateWithTrueOverwrite()  // this is equivalent of using the master_grid pointer.

   // master_array - is a direct pointer to the resulting master_grid...?
*/
    unsigned char * master_array = master_grid.getCharMap();
//    unsigned char * local_array = costmap_.getCharMap();
    unsigned int size_x = master_grid.getSizeInCellsX(), size_y = master_grid.getSizeInCellsY();
    bool showed_log = false;
    min_i = std::max(0, min_i);
    min_j = std::max(0, min_j);
    max_i = std::min(static_cast<int>(size_x), max_i);
    max_j = std::min(static_cast<int>(size_y), max_j);
    // this is where i will start putting my own logic.
    int gradient_index;
    for (int j = min_j; j < max_j; j++){
        gradient_index = 0;
        for (int i = min_i; i < max_i; i++){
            int index = master_grid.getIndex(i, j);
//            int local_index = costmap_.getIndex(i, j);
        // shouldn't the cost be calculated after setting gradient_index?
            unsigned char cost = LETHAL_OBSTACLE - gradient_index*GRADIENT_FACTOR%255;
            if (gradient_index <= GRADIENT_SIZE) {
                gradient_index++;
            } else {
                gradient_index = 0;
            }
            master_array[index] = cost;

            if (!showed_log){
                showed_log = true;
                RCLCPP_INFO(rclcpp::get_logger("nav2_costmap_2d"),
                "TutorialLayer::updateCosts() Has found index %i", index);
            }
        }
    }
}

}

#include "pluginlib/class_list_macros.hpp"
PLUGINLIB_EXPORT_CLASS(nav2_plugin_tutorial::TutorialLayer, nav2_costmap_2d::Layer)
