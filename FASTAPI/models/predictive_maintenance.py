
import numpy as np
import logging
import matplotlib.pyplot as plt


class VehicleMaintenance:
    def __init__(self, **kwargs):
        # Initialize vehicle parameters
        self.distance_traveled = kwargs.get("distance_w_mil", 0)
        self.time_in_years = kwargs.get("time_in_years", 1)
        self.speed = kwargs.get("speed", 0)
        self.engine_load = kwargs.get("engine_load", 50)
        self.coolant_temp = kwargs.get("coolant_temp", 90)
        self.engine_runtime = kwargs.get("run_time", 0)
        self.service_interval = 10000
        self.throttle_pos = kwargs.get("throttle_pos", 0)
        self.fuel_level = kwargs.get("fuel_level", 50)
        self.short_fuel_trim = kwargs.get("short_fuel_trim_1", 0)
        self.long_fuel_trim = kwargs.get("long_fuel_trim_1", 0)
        self.ambient_air_temp = kwargs.get("ambient_air_temp", 25)
        self.o2_sensor_reading = kwargs.get("o2_sensors", 0.5)
        self.catalyst_temp = kwargs.get("catalyst_temp_b1s1", 350)

    def estimate_tire_wear(self) -> float:
        """Estimate tire wear based on distance traveled and vehicle age."""
        try:
            # Simple tire wear estimation logic
            wear_rate = 0.1  # Arbitrary wear rate per 1000 miles
            tire_wear = self.distance_traveled * wear_rate / 1000
            # Ensure tire wear does not exceed 100%
            return min(tire_wear, 100)
        except Exception as e:
            logging.error(f"Error estimating tire wear: {e}")
            return 0.0

    def predict_spark_plug_replacement(self) -> str:
        try:
            age_factor = self.time_in_years / 2  # Typical 2-year replacement interval
            distance_factor = self.distance_traveled / 100000
            wear_threshold = 1.0  # Summation of factors that would suggest replacement
            if age_factor + distance_factor > wear_threshold:
                return "Replace spark plugs soon."
            return "Spark plugs in good condition."
        except Exception as e:
            logging.error(f"Error predicting spark plug replacement: {e}")
            return "Unable to assess spark plug condition."

    def predict_coolant_condition(self) -> str:
        try:
            if self.coolant_temp >= 100:
                return "Coolant condition is poor; consider changing."
            return "Coolant condition is acceptable."
        except Exception as e:
            logging.error(f"Error predicting coolant condition: {e}")
            return "Unable to assess coolant condition."

    def estimate_oil_change(self) -> str:
        try:
            if self.engine_runtime >= 5000:
                return "Oil change needed soon."
            return "Oil condition is acceptable."
        except Exception as e:
            logging.error(f"Error estimating oil change: {e}")
            return "Unable to assess oil condition."

    def estimate_brake_pad_wear(self) -> float:
        # Placeholder for brake pad wear estimation logic
        return 90.0  # Assume 90% remaining life for demonstration

    def assess_battery_health(self) -> str:
        try:
            if self.control_module_voltage < 12.0:
                return "Battery health is poor; consider replacement."
            return "Battery healthy."
        except Exception as e:
            logging.error(f"Error assessing battery health: {e}")
            return "Unable to determine battery health."

    def fuel_system_maintenance(self) -> str:
        try:
            short_trim_issue = abs(self.short_fuel_trim) > 10
            long_trim_issue = abs(self.long_fuel_trim) > 10
            low_fuel = self.fuel_level < 15

            if short_trim_issue and long_trim_issue and low_fuel:
                return "Fuel system needs immediate service."
            elif (short_trim_issue or long_trim_issue) and low_fuel:
                return "Fuel system needs inspection soon."
            elif short_trim_issue or long_trim_issue:
                return "Monitor fuel system performance."
            return "Fuel system operating normally."
        except Exception as e:
            logging.error(f"Error checking fuel system: {e}")
            return "Unable to determine fuel system condition."

    def air_filter_replacement(self) -> str:
        try:
            distance_factor = self.distance_traveled / 10000
            temp_stress = max(0, (self.ambient_air_temp - 25) / 30)
            load_factor = self.engine_load / 75
            condition_score = distance_factor * (1 + temp_stress) * load_factor

            if condition_score > 1.5:
                return "Replace air filter immediately."
            elif condition_score > 1.2:
                return "Replace air filter very soon."
            elif condition_score > 1.0:
                return "Replace air filter soon."
            return "Air filter condition good."
        except Exception as e:
            logging.error(f"Error checking air filter: {e}")
            return "Unable to determine air filter condition."

    def exhaust_system_check(self) -> str:
        try:
            o2_reading = float(self.o2_sensor_reading)
            cat_temp = float(self.catalyst_temp)
            o2_sensor_issue = o2_reading < 0.5 or o2_reading > 1.5
            cat_temp_issue = cat_temp < 300 or cat_temp > 900

            if o2_sensor_issue and cat_temp_issue:
                return "Exhaust system needs immediate inspection."
            elif o2_sensor_issue:
                return "O2 sensor may need replacement."
            elif cat_temp_issue:
                return "Catalytic converter may need inspection."
            return "Exhaust system operating normally."
        except ValueError:
            return "Invalid exhaust sensor readings."
        except Exception as e:
            logging.error(f"Error checking exhaust system: {e}")
            return "Unable to determine exhaust system condition."

    def suspension_system_maintenance(self) -> str:
        try:
            distance_factor = self.distance_traveled / 20000
            speed_stress = max(0, (self.speed - 80) / 100)
            load_stress = self.throttle_pos / 75
            wear_score = distance_factor * (1 + speed_stress + load_stress)

            if wear_score > 1.5:
                return "Suspension needs immediate inspection."
            elif wear_score > 1.2:
                return "Suspension needs inspection soon."
            elif wear_score > 1.0:
                return "Monitor suspension condition."
            return "Suspension system okay."
        except Exception as e:
            logging.error(f"Error checking suspension: {e}")
            return "Unable to determine suspension condition."

    def wheel_alignment(self) -> str:
        try:
            distance_factor = self.distance_traveled / 15000
            tire_wear = (100 - self.estimate_tire_wear()) / 100
            alignment_score = distance_factor + tire_wear

            if alignment_score > 1.5:
                return "Wheel alignment needed immediately."
            elif alignment_score > 1.2:
                return "Wheel alignment needed very soon."
            elif alignment_score > 1.0:
                return "Consider wheel alignment check."
            return "Wheel alignment okay."
        except Exception as e:
            logging.error(f"Error checking wheel alignment: {e}")
            return "Unable to determine alignment condition."

    def fuel_economy_monitoring(self) -> str:
        try:
            low_fuel = self.fuel_level < 10
            high_load = self.engine_load > 80
            trim_issues = abs(self.short_fuel_trim) > 10 or abs(self.long_fuel_trim) > 10

            if low_fuel and high_load and trim_issues:
                return "Significant fuel economy issues detected."
            elif (low_fuel and high_load) or trim_issues:
                return "Possible fuel economy issues."
            elif low_fuel or high_load:
                return "Monitor fuel economy."
            return "Fuel economy normal."
        except Exception as e:
            logging.error(f"Error monitoring fuel economy: {e}")
            return "Unable to determine fuel economy status."

    def evaporative_emission_system_check(self) -> str:
        """Check the evaporative emission system for potential issues."""
        try:
            # Simple checks for evap system based on fuel level and ambient temperature
            low_fuel = self.fuel_level < 10
            temp_stress = self.ambient_air_temp > 30
            system_stress = abs(self.short_fuel_trim) > 10

            if low_fuel and temp_stress and system_stress:
                return "Evap system needs immediate inspection."
            elif (low_fuel and temp_stress) or system_stress:
                return "Monitor evap system condition."
            elif low_fuel or temp_stress:
                return "Evap system may need future inspection."
            return "Evap system operating normally."
        except Exception as e:
            logging.error(f"Error checking evap system: {e}")
            return "Unable to determine evap system condition."

    def visualize_vehicle_maintenance(self):
        """Visualize vehicle maintenance metrics as bar charts."""
        try:
            labels = ['Fuel Level', 'Tire Wear', 'Engine Load']
            # Collect data for visualization
            data = [self.fuel_level, self.estimate_tire_wear(), self.engine_load]
            plt.bar(labels, data)
            plt.title('Vehicle Maintenance Metrics')
            plt.ylabel('Percentage / Value')
            plt.ylim([0, 100])
            plt.show()
        except Exception as e:
            logging.error(f"Error during visualization: {e}")

    def generate_report(self) -> dict:
        """
        Generate a maintenance report summarizing the vehicle's status.
        """
        report = {
            "Distance Traveled": self.distance_traveled,
            "Time in Years": self.time_in_years,
            "Speed": self.speed,
            "Engine Load": self.engine_load,
            "Coolant Temperature": self.coolant_temp,
            "Engine Runtime": self.engine_runtime,
            "Fuel Level": self.fuel_level,
            "Spark Plug Status": self.predict_spark_plug_replacement(),
            "Coolant Status": self.predict_coolant_condition(),
            "Oil Change Needed": self.estimate_oil_change(),
            "Brake Pad Wear": self.estimate_brake_pad_wear(),
            "Battery Status": self.assess_battery_health(),
            "Fuel System Status": self.fuel_system_maintenance(),
            "Air Filter Status": self.air_filter_replacement(),
            "Exhaust System Status": self.exhaust_system_check(),
            "Suspension Status": self.suspension_system_maintenance(),
            "Wheel Alignment Status": self.wheel_alignment(),
            "Fuel Economy": self.fuel_economy_monitoring(),
            "Evaporative Emission System Status": self.evaporative_emission_system_check(),
        }

        return report