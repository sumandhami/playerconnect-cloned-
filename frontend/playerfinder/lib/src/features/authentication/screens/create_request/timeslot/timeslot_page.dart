import 'package:flutter/material.dart';

class TimeSlotPage extends StatefulWidget {
  final String venue;
  const TimeSlotPage({required this.venue});

  @override
  _TimeSlotPageState createState() => _TimeSlotPageState();
}

class _TimeSlotPageState extends State<TimeSlotPage> {
  List<Map<String, dynamic>> timeSlots = [
    {
      "startTime": "5:00 PM",
      "endTime": "6:00 PM",
      "players": 4,
      "selectedPlayers": []
    },
    {
      "startTime": "6:00 PM",
      "endTime": "7:00 PM",
      "players": 9,
      "selectedPlayers": []
    },
    {
      "startTime": "7:00 PM",
      "endTime": "8:00 PM",
      "players": 7,
      "selectedPlayers": []
    },
  ];

  List<String> friendsList = ["John", "Alex", "Sam", "Mike", "Chris", "Leo"];

  void _openPlayerSelection(int index) {
    showDialog(
      context: context,
      builder: (context) {
        List<String> selectedPlayers =
            List<String>.from(timeSlots[index]["selectedPlayers"] ?? []);

        return AlertDialog(
          title: Text("Add Players (${timeSlots[index]["players"]}/15)"),
          content: StatefulBuilder(
            builder: (context, setModalState) {
              return Column(
                mainAxisSize: MainAxisSize.min,
                children: friendsList.map((friend) {
                  bool isSelected = selectedPlayers.contains(friend);
                  return CheckboxListTile(
                    title: Text(friend),
                    value: isSelected,
                    onChanged: (bool? value) {
                      setModalState(() {
                        if (value == true &&
                            selectedPlayers.length +
                                    timeSlots[index]["players"] <
                                15) {
                          selectedPlayers.add(friend);
                        } else if (value == false) {
                          selectedPlayers.remove(friend);
                        }
                      });
                    },
                  );
                }).toList(),
              );
            },
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: Text("Cancel"),
            ),
            ElevatedButton(
              onPressed: () {
                setState(() {
                  int previousPlayers =
                      timeSlots[index]["selectedPlayers"]?.length ?? 0;
                  int newPlayers = selectedPlayers.length - previousPlayers;

                  timeSlots[index]["players"] += newPlayers;
                  timeSlots[index]["selectedPlayers"] = selectedPlayers;
                });
                Navigator.pop(context);
              },
              child: Text("Confirm"),
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Time Slots - ${widget.venue}"),
        backgroundColor: Color(0xFF1B2A41),
        foregroundColor: Colors.grey.shade300,
      ),
      body: Container(
        width: double.infinity,
        height: double.infinity,
        decoration: BoxDecoration(
          gradient: RadialGradient(
            center: Alignment.center,
            radius: 0.9,
            colors: [
              Color(0xFF1B2A41),
              Color(0xFF23395B),
              Color(0xFF2D4A69),
            ],
            stops: [0.3, 0.7, 1.0],
          ),
        ),
        child: ListView.builder(
          itemCount: timeSlots.length,
          itemBuilder: (context, index) {
            final slot = timeSlots[index];
            final int playerCount = slot["players"];
            String status = playerCount < 10
                ? "Occupying..."
                : playerCount < 15
                    ? "Booking..."
                    : "Fully Booked";

            return GestureDetector(
              onTap:
                  playerCount < 15 ? () => _openPlayerSelection(index) : null,
              child: Container(
                margin: EdgeInsets.all(10),
                padding: EdgeInsets.all(15),
                decoration: BoxDecoration(
                  color: playerCount >= 15 ? Colors.grey : Color(0xFF1E3A5F),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: ListTile(
                  title: Text("${slot['startTime']} - ${slot['endTime']}",
                      style: TextStyle(color: Colors.white)),
                  subtitle: Text("$playerCount / 15 players - $status",
                      style: TextStyle(color: Colors.grey.shade300)),
                  trailing: playerCount >= 15
                      ? Icon(Icons.lock, color: Colors.red)
                      : Icon(Icons.person_add, color: Colors.green),
                ),
              ),
            );
          },
        ),
      ),
    );
  }
}
