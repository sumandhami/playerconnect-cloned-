import 'package:flutter/material.dart';

class JoinRequest extends StatelessWidget {
  const JoinRequest({super.key});

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Scaffold(
        appBar: AppBar(
          leading: IconButton(
            icon: Icon(Icons.arrow_back),
            onPressed: () {
              Navigator.pop(context);
            },
          ),
          title: Text("List of requests"),
        ),
      ),
    );
  }
}
