import 'package:flutter/material.dart';
import 'package:tender_app_windy/src/common_widgets/explore_people_app_bar_widget.dart';
import 'package:tender_app_windy/src/theme_manager/values_manager.dart';

class ExplorePeopleScreen extends StatefulWidget {
  static const String routeName = '/explore-people';
  const ExplorePeopleScreen({super.key});

  @override
  State<ExplorePeopleScreen> createState() => _ExplorePeopleScreenState();
}

class _ExplorePeopleScreenState extends State<ExplorePeopleScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Padding(
        padding: EdgeInsets.symmetric(
            vertical: AppPadding.p40, horizontal: AppPadding.p24),
        child: Column(
          children: const [ExplorePeopleAppBarWidget()],
        ),
      ),
    );
  }
}
