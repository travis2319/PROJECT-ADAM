export interface EmissionsData {
    summary: {
      total_vehicle_values: number;
      compliant_vehicle_values: number;
      non_compliant_vehicle_values: number;
      compliance_rate: number;
      start_timestamp: string;
      end_timestamp: string;
      total_distance_traveled: number;
      total_records: number;
      good_condition: number;
      needs_attention: number;
      health_rate: number;
    };
  }
  
  export interface HealthMonitoringData {
    summary: {
      total_vehicle_values: number;
      compliant_vehicle_values: number;
      non_compliant_vehicle_values: number;
      compliance_rate: number;
      start_timestamp: string;
      end_timestamp: string;
      total_distance_traveled: number;
      total_records: number;
      good_condition: number;
      needs_attention: number;
      health_rate: number;
    };
  }
  
  export interface PredictiveMaintenanceData {
    summary: {
      timestamp: string;
      total_vehicles: number;
      status_distribution: {
        Critical: number;
        Warning: number;
        Good: number;
      };
      critical_systems: {
        engine: number;
        coolant: number;
        fuel: number;
        brake_wear: number;
      };
      maintenance_required: {
        immediate_attention: number;
        soon_attention: number;
        good_condition: number;
      };
    };
  }