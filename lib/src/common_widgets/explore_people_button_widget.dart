import 'package:flutter/material.dart';
import 'package:tender_app_windy/src/common_widgets/match_button_widget.dart';

class ExplorePeopleButtonWidget extends StatelessWidget {
  const ExplorePeopleButtonWidget({super.key});

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
      children: [
        MatchButtonWidget(
          iconPath: 'icon_close.png',
          onTap: () {},
        ),
        MatchButtonWidget(
          dimension: 80.0,
          iconPath: 'icon_love.png',
          onTap: () {},
        ),
        MatchButtonWidget(
          iconPath: 'icon_favorite.png',
          onTap: () {},
        ),
      ],
    );
  }
}
