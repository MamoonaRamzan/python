import re
import heapq
from datetime import datetime, timedelta
from collections import defaultdict


LOG_PATTERN = re.compile(
    r"\[(.*?)\] \[(.*?)\] \[(.*?)\] (.*)\((E\d{4}|W\d{4})\)"
)


def parse_log_line(line):
    match = LOG_PATTERN.search(line)
    if match:
        timestamp_str, level, service, message, code = match.groups()
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        return {
            "timestamp": timestamp,
            "level": level,
            "service": service,
            "message": message.strip(),
            "code": code
        }
    return None


PRIORITY_MAP = {
    "CRITICAL": 1,
    "ERROR": 2,
    "WARNING": 3,
    "INFO": 4
}


def analyze_logs(file_path, start_time, end_time):
    errors = []
    service_summary = defaultdict(lambda: {"count": 0, "codes": set()})
    critical_errors = defaultdict(list)

    
    with open(file_path, "r") as file:
        for line in file:
            log = parse_log_line(line)
            if not log:
                continue

            if not (start_time <= log["timestamp"] <= end_time):
                continue

            service_summary[log["service"]]["count"] += 1
            service_summary[log["service"]]["codes"].add(log["code"])

            if log["level"] in ["CRITICAL", "ERROR", "WARNING"]:
                heapq.heappush(errors, (PRIORITY_MAP[log["level"]], log["timestamp"], log))

            if log["level"] == "CRITICAL":
                critical_errors[(log["service"], log["code"])].append(log["timestamp"])

    return errors, service_summary, critical_errors


def generate_report(errors, service_summary, critical_errors, start_time, end_time):
    print(f"Log Analysis Report ({start_time} to {end_time})")
    print("\nTop Critical Issues (Priority Order):")
    ranked = []
    for (service, code), times in critical_errors.items():
        ranked.append((len(times), service, code, times))
    ranked.sort(reverse=True)

    for i, (count, service, code, times) in enumerate(ranked, 1):
        print(f"{i}. [CRITICAL] {service}: {code} - {count} occurrence{'s' if count > 1 else ''}")
        print(f"First occurrence: {times[0]}")
        if count > 1:
            print(f"Last occurrence: {times[-1]}")
            avg_diff = (times[-1] - times[0]) / (count - 1)
            print(f"Average time between occurrences: {avg_diff}")
        else:
            print(f"Occurrence: {times[0]}")
        print()

    print("Error Distribution by Service:")
    for service, info in service_summary.items():
        level_counts = f"{info['count']} error{'s' if info['count'] > 1 else ''}"
        code_count = len(info["codes"])
        print(f"- {service}: {level_counts} ({code_count} unique error codes)")

    print("\nTimeline Visualization:")
    timeline = defaultdict(list)
    for _, _, log in errors:

        hour = log["timestamp"].strftime("%H:00")
        timeline[hour].append(log["code"])

    for hour in sorted(timeline.keys()):
        codes = " ".join(timeline[hour])
        print(f"{hour}: {codes}")

    print("\nRecommended Actions:")
    for (service, code), logs in critical_errors.items():
        if len(logs) > 1:
            print(f"1. Investigate recurring {service} issues ({code})")
    if any("AUTH-SERVICE" in key[0] and key[1] == "E4001" for key in critical_errors.keys()):
        print("2. Check AUTH-SERVICE for repeated login failures (E4001)")


if __name__ == "__main__":
    start = datetime(2023, 3, 1, 8, 0, 0)
    end = datetime(2023, 3, 1, 12, 30, 0)
    errors, summary, criticals = analyze_logs("server_logs.txt", start, end)
    generate_report(errors, summary, criticals, start, end)
