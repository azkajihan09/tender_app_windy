import 'package:flutter/material.dart';

import 'package:tender_app_windy/src/theme_manager/style_manager.dart';

class CustomTextButtonWidget extends StatelessWidget {
  const CustomTextButtonWidget({
    Key? key,
    required this.title,
    required this.onPressed,
  }) : super(key: key);

  final String title;
  final VoidCallback onPressed;

  @override
  Widget build(BuildContext context) {
    return TextButton(
        onPressed: onPressed,
        child: Text(
          title,
          style: getBlack30TextStyle().copyWith(
            decoration: TextDecoration.underline,
          ),
        ));
  }
}
