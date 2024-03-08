#include "nav2_plugin_tutorial/tutorial_costmap_plugin.hpp"

#include "nav2_costmap_2d/costmap_math.hpp"
#include "nav2_costmap_2d/footprint.hpp"
#include "rclcpp/parameter_events_filter.hpp"

using nav2_costmap_2d::LETHAL_OBSTACLE;

namespace nav2_plugin_tutorial{

// I think these are the bounds of the last updated section of the map?
TutorialLayer::TutorialLayer():
last_min_x_(-std::numeric_limits<float>::max()),
last_min_y_(-std::numeric_limits<float>::max()),
last_max_x_(std::numeric_limits<float>::max()),
last_max_y_(std::numeric_limits<float>::max())
{}

//Method to call, at the end of initialization.
void TutorialLayer::onInitialize(){
    auto node = node_.lock();
    declareParameter("enabled", rclcpp::ParameterValue(true));
    node->get_parameter(name_ + ".enabled", enabled_);

    need_recalculation_ = false;
    current_ = true;
}
// The method to calculate which section of the map needs recalculations
// input is robot position (with 3 variables), output is bounding box (4 values, 2 koordinates).
// Both are currently input? - probably some cpp magic
void TutorialLayer::updateBounds(double robot_x, double robot_y, double robot_yaw,
double * min_x, double * min_y, double * max_x , double * max_y){
    if (need_recalculation_) {
        last_min_x_ = *min_x;
        last_min_y_ = *min_y;
        last_max_x_ = *max_x;
        last_max_y_ = *max_y;

        *min_x = -std::numeric_limits<float>::max();
        *min_y = -std::numeric_limits<float>::max();
        *max_x = -std::numeric_limits<float>::max();
        *max_y = -std::numeric_limits<float>::max();
        need_recalculation_ = false;
    } else {
        double tmp_min_x = last_min_x_;
        double tmp_min_y = last_min_y_;
        double tmp_max_x = last_max_x_;
        double tmp_max_y = last_max_y_;

        last_min_x_ = *min_x;
        last_min_y_ = *min_y;
        last_max_x_ = *max_x;
        last_max_y_ = *max_y;

        *min_x = std::min(tmp_min_x, *min_x);
        *min_y = std::min(tmp_min_y, *min_y);
        *max_x = std::max(tmp_max_x, *max_x);
        *max_y = std::max(tmp_max_y, *max_y);
    }
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
