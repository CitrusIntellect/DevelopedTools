#!/bin/bash

# Function to send notification
send_notification() {
    local urgency=$1
    local message=$2
    notify-send -u "$urgency" "System Usage Alert" "$message"
}

# Function to get CPU usage percentage
get_cpu_usage() {
    # Get the average CPU usage over a 1-second interval
    mpstat 1 1 | awk '/Average/ {print 100 - $NF}'
}

# Function to get memory usage percentage
get_memory_usage() {
    # Calculate memory usage percentage using free command
    free | awk '/Mem/ {printf("%.2f"), $3/$2 * 100}'
}

# Define thresholds
cpu_warning_threshold=75
cpu_critical_threshold=90
memory_warning_threshold=75
memory_critical_threshold=90

# Flags to prevent multiple notifications
cpu_warning_sent=false
cpu_critical_sent=false
memory_warning_sent=false
memory_critical_sent=false

# Reset threshold after usage drops below threshold
reset_threshold_time=10  # Seconds of low usage before resetting notification

# Infinite loop to check every 30 seconds
while true; do
    # Get CPU and memory usage
    cpu_usage=$(get_cpu_usage)
    memory_usage=$(get_memory_usage)

    # Check CPU usage and send notification if necessary
    if (( $(echo "$cpu_usage > $cpu_critical_threshold" | bc -l) )); then
        if [ "$cpu_critical_sent" = false ]; then
            send_notification "critical" "CRITICAL: CPU usage is at $cpu_usage%"
            cpu_critical_sent=true
        fi
    elif (( $(echo "$cpu_usage > $cpu_warning_threshold" | bc -l) )); then
        if [ "$cpu_warning_sent" = false ] && [ "$cpu_critical_sent" = false ]; then
            send_notification "normal" "Warning: CPU usage is at $cpu_usage%"
            cpu_warning_sent=true
        fi
    else
        # CPU usage has dropped, reset flags after a brief delay
        if [ "$cpu_critical_sent" = true ] || [ "$cpu_warning_sent" = true ]; then
            sleep $reset_threshold_time
            if (( $(echo "$cpu_usage <= $cpu_warning_threshold" | bc -l) )); then
                cpu_critical_sent=false
                cpu_warning_sent=false
            fi
        fi
    fi

    # Check memory usage and send notification if necessary
    if (( $(echo "$memory_usage > $memory_critical_threshold" | bc -l) )); then
        if [ "$memory_critical_sent" = false ]; then
            send_notification "critical" "CRITICAL: Memory usage is at $memory_usage%"
            memory_critical_sent=true
        fi
    elif (( $(echo "$memory_usage > $memory_warning_threshold" | bc -l) )); then
        if [ "$memory_warning_sent" = false ] && [ "$memory_critical_sent" = false ]; then
            send_notification "normal" "Warning: Memory usage is at $memory_usage%"
            memory_warning_sent=true
        fi
    else
        # Memory usage has dropped, reset flags after a brief delay
        if [ "$memory_critical_sent" = true ] || [ "$memory_warning_sent" = true ]; then
            sleep $reset_threshold_time
            if (( $(echo "$memory_usage <= $memory_warning_threshold" | bc -l) )); then
                memory_critical_sent=false
                memory_warning_sent=false
            fi
        fi
    fi

    # Sleep for 30 seconds before checking again
    sleep 30
done
