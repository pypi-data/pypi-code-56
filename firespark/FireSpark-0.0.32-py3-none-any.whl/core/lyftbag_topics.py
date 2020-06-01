from ..protos.src.backend.bigquery.test_av_bigquery_table_pb2 import TestAvBigqueryTable
from ..protos.src.control.messages.control_service_state_pb2 import ControlServiceState
from ..protos.src.slam.proto.slam_performance_pb2 import SlamPerformance
from ..protos.src.avs.messages.diagnostics_message_pb2 import DiagnosticsMessage
from ..protos.src.planning.proto.planning_diagnostic_pb2 import PlanningDiagnosticProto
from ..protos.src.planning.proto.handler_data_pb2 import HandlerDataMessage
from ..protos.src.planning.proto.planning_debug_pb2 import PlanningDebugProto
from ..protos.src.planning.proto.planning_debug_pb2 import DebugValue
# from ..protos.src.planning.proto.nudge_metrics_pb2 import NudgeMetricsProto
from ..protos.src.perception.proto.perception_obstacles_pb2 import PerceptionObstacles
from ..protos.src.perception.proto.radar_output_pb2 import RadarOutputProto
from ..protos.src.prediction.messages.prediction_timing_pb2 import PredictionTimingProto
from ..protos.src.avs.messages.mission_pb2 import Mission
from ..protos.src.vehicle.fusion.message.vehicle_command_pb2 import VehicleCommand
from ..protos.src.vehicle.fusion.message.vehicle_report_pb2 import VehicleReport
from ..protos.src.slam.services.proto.deltas_pb2 import TimestampedPoseDelta
from ..protos.src.observability.cpu.message.cpu_report_pb2 import CpuReport
from ..protos.src.observability.gpu.message.gpu_report_pb2 import GpuReport
from ..protos.src.observability.disk.message.disk_report_pb2 import DiskReport
from ..protos.src.observability.sensors.message.sensors_observability_pb2 import SensorsInformation
from ..protos.src.avs.messages.runtime_metrics_pb2 import SpikeRuntimeMetricsMessage
from ..protos.src.avs.messages.service_timing_message_pb2 import ServiceTimingMessage
from ..protos.src.avs.messages.subscriber_rx_timing_message_pb2 import SubscriberRxTimingMessage
from ..protos.src.avs.messages.lyftbag_pb2 import WriterStats
from ..protos.src.carviz.proto.notes_pb2 import NoteMessage
from ..protos.src.carviz.proto.carviz_fps_pb2 import CarvizFps
from ..protos.src.carviz.proto.carviz_init_timing_stats_pb2 import CarvizInitTimingStats
from ..protos.src.avs.messages.carviz_timing_pb2 import CarvizTiming
from ..protos.src.avs.messages.disengagement_report_message_pb2 import DisengagementReport
from ..protos.src.perception.proto.traffic_light_output_pb2 import TrafficLightOutputProto
from ..protos.src.perception.proto.traffic_light_output_pb2 import TrafficLightDetectionWithMapAssociation
from ..protos.src.sensor.camera.proto.image_pb2 import CompressedImage
from ..protos.src.sensor.gnss.proto.ins_pb2 import RawImu, InsPva, CorrImu, GnssBestPosition
from ..protos.src.sensor.lidar.proto.lidar_pb2 import LidarPacketList
from ..protos.src.sensor.proto.sensor_info_pb2 import SensorInfo
from ..protos.src.vision.proto.vision_output_pb2 import VisionOutputProto
from ..protos.src.calibration.lib_calibration.calibration_quality_metrics_pb2 import CalibrationQualityMetricsProto
from ..protos.src.sensor.radar.proto.radar_pb2 import RadarPacketList
from ..protos.src.localization.proto.jerk_pb2 import JerkProto
from ..protos.src.calibration.lib_calibration.calibration_pb2 import VehicleCalibrationProto
from ..protos.src.localization.proto.localization_debug_state_pb2 import LocalizationDebugState
from ..protos.src.planning.proto.planned_trajectory_pb2 import PlannedTrajectoryProto
from ..protos.src.common.kinematics.proto.motionstate3d_pb2 import MotionState3DProto
# from ..protos.src.slam.services.proto.health_pb2 import LocalizationHealth
# from ..protos.src.calibration.lib_calibration.calibration_quality_metrics_pb2 import YawMisalignmentFromMotionStateInfo
# from ..protos.src.calibration.lib_calibration.calibration_quality_metrics_pb2 import OnlineImuDebugStatesProto
# from ..protos.src.avs.services.performance_monitor.messages.system_performance_report_pb2 import SystemPerformanceReport
# from ..protos.src.avs.services.performance_monitor.messages.process_performance_report_pb2 import ProcessPerformanceReport

SUPPORTED_TOPICS = {
    '/control/state': ControlServiceState,
    '/test/av/bigquery/table': TestAvBigqueryTable,
    '/localization/slam_performance': SlamPerformance,
    '/avs/carviz/fps': CarvizFps,
    '/avs/carviz/plugin_timing_stats': CarvizTiming,
    '/avs/carviz/init_timing_stats': CarvizInitTimingStats,
    '/avs/diagnostics': DiagnosticsMessage,
    '/planning/diagnostic': PlanningDiagnosticProto,
    '/planning/debug': PlanningDebugProto,
    '/planning/handler_data': HandlerDataMessage,
    # '/planning/nudge_metrics': NudgeMetricsProto,
    '/perception/perception_obstacles': PerceptionObstacles,
    '/prediction/timing': PredictionTimingProto,
    '/avs/mission': Mission,
    '/vehicle_report/steering': VehicleReport,
    '/vehicle_report/throttle': VehicleReport,
    '/vehicle_report/brake': VehicleReport,
    '/vehicle_report/autonomy_event': VehicleReport,
    '/vehicle_report/is_stationary': VehicleReport,
    '/vehicle_report/speed': VehicleReport,
    '/vehicle_report/wheel_speed': VehicleReport,
    '/vehicle_command/throttle': VehicleCommand,
    '/vehicle_command/brake': VehicleCommand,
    '/vehicle_command/steering': VehicleCommand,
    '/localization/metrics/global_pose_jumpiness': TimestampedPoseDelta,
    '/cpu_monitoring': CpuReport,
    '/gpu_monitoring': GpuReport,
    '/disk_monitoring': DiskReport,
    '/sensors_monitoring': SensorsInformation,
    '/avs/service_timing_stats': ServiceTimingMessage,
    '/avs/spike_runtime_metrics': SpikeRuntimeMetricsMessage,
    '/avs/subscriber_timing': SubscriberRxTimingMessage,
    '/logger/writer_stats': WriterStats,
    '/avs/notes': NoteMessage,
    '/avs/disengagement_report': DisengagementReport,
    '/perception/traffic_light_output': TrafficLightOutputProto,
    '/perception/traffic_light_joint_output': TrafficLightOutputProto,
    '/cam0/image_compressed': CompressedImage,
    '/cam1/image_compressed': CompressedImage,
    '/cam2/image_compressed': CompressedImage,
    '/cam3/image_compressed': CompressedImage,
    '/cam4/image_compressed': CompressedImage,
    '/cam5/image_compressed': CompressedImage,
    '/cam6/image_compressed': CompressedImage,
    '/cam7/image_compressed': CompressedImage,
    '/cam8/image_compressed': CompressedImage,
    '/gammera0/image_compressed': CompressedImage,
    '/gammera1/image_compressed': CompressedImage,
    '/gammera2/image_compressed': CompressedImage,
    '/gammera3/image_compressed': CompressedImage,
    '/gammera4/image_compressed': CompressedImage,
    '/gammera5/image_compressed': CompressedImage,
    '/gammera6/image_compressed': CompressedImage,
    '/novatel/rawimu': RawImu,
    '/novatel/corrimu': CorrImu,
    '/novatel/inspva': InsPva,
    '/lidar_packet_lists': LidarPacketList,
    '/lidar0/lidar_packet_lists': LidarPacketList,
    '/lidar1/lidar_packet_lists': LidarPacketList,
    '/lidar2/lidar_packet_lists': LidarPacketList,
    '/lidar3/lidar_packet_lists': LidarPacketList,
    '/lidar4/lidar_packet_lists': LidarPacketList,
    '/lidar5/lidar_packet_lists': LidarPacketList,
    '/sensor_info': SensorInfo,
    '/vision/vision_2d_obstacles': VisionOutputProto,
    '/calibration/metrics': CalibrationQualityMetricsProto,
    '/astyx_radar0/raw_data': RadarPacketList,
    '/astyx_radar1/raw_data': RadarPacketList,
    '/astyx_radar2/raw_data': RadarPacketList,
    '/astyx_radar3/raw_data': RadarPacketList,
    '/astyx_radar4/raw_data': RadarPacketList,
    '/perception/radar_obstacles': RadarOutputProto,
    '/novatel/gnsspos': GnssBestPosition,
    '/localization/jerk': JerkProto,
    '/monitor_metrics/steering_wheel_angle_rate': DebugValue,
    '/monitor_metrics/steering_wheel_angle_2nd_derivative': DebugValue,
    '/monitor_metrics/steering_wheel_angle_rate_radps': DebugValue,
    '/monitor_metrics/steering_wheel_angle_2nd_derivative_radps2': DebugValue,
    '/monitor_metrics/ego_heading_rad': DebugValue,
    '/monitor_metrics/reference_line_direction_rad': DebugValue,
    '/monitor_metrics/reference_line_curvature': DebugValue,
    '/monitor_metrics/ego_heading_diff_from_reference_line_rad': DebugValue,
    '/monitor_metrics/cross_distance_from_reference_line_m': DebugValue,
    '/calibration': VehicleCalibrationProto,
    '/perception/traffic_light_detection': TrafficLightDetectionWithMapAssociation,
    '/localization/debug_state': LocalizationDebugState,
    '/planning': PlannedTrajectoryProto,
    '/localization/motion_state': MotionState3DProto,
    # '/localization/health': LocalizationHealth,
    '/localization/global_slam_world_from_vehicle': MotionState3DProto,
    # '/calibration/yawmisalignment_ins': YawMisalignmentFromMotionStateInfo,
    # '/calibration/yawmisalignment_smooth': YawMisalignmentFromMotionStateInfo,
    # '/calibration/online_imu_debug_states': OnlineImuDebugStatesProto,
    # '/performance/system': SystemPerformanceReport,
    # '/performance/processes': ProcessPerformanceReport,
}
