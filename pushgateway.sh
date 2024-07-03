#!/bin/bash

while true; do
    # Get the list of running domains and their UUIDs
    running_domains=$(virsh list --all --name --uuid --state-running)

    # Initialize an array to store domain data
    domains_data=()

    # Iterate over each line (domain) in the list
    while IFS= read -r line; do
        # Extract domain name and UUID from the line
        domain_uuid=$(echo "$line" | awk '{print $1}')
        domain_name=$(echo "$line" | awk '{print $2}')
        disk_num=$(virsh domblklist "$domain_name" | grep -c 'disk')
        # Get domain statistics and remove '\n' characters
        domstats_output=$(virsh domstats "$domain_uuid" | jq -sR '.')

        # Add domain data to the array
        domains_data+=("{ \"domain_name\": \"$domain_name\", \"domain_uuid\": \"$domain_uuid\",\"disk_num\": $disk_num, \"domstats_output\": $domstats_output }")

    done <<< "$running_domains"

    # Combine all domain data into a single JSON array
    json_data="[$(IFS=,; echo "${domains_data[*]}")]"

    # Send a single POST request with JSON data
    curl -X POST -H "Content-Type: application/json" -d "$json_data" "http://192.168.15.21:5000/endpoint"

    # Sleep for 10 seconds before the next iteration
    sleep 10
done