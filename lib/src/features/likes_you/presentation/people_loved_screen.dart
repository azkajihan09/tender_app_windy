import 'package:flutter/material.dart';
import 'package:tender_app_windy/src/common_widgets/poeple_loved_card.dart';
import 'package:tender_app_windy/src/theme_manager/font_manager.dart';
import 'package:tender_app_windy/src/theme_manager/style_manager.dart';
import 'package:tender_app_windy/src/theme_manager/values_manager.dart';

class PeopleLoveScreen extends StatefulWidget {
  static const String routeName = '/people-loved';
  const PeopleLoveScreen({super.key});

  @override
  State<PeopleLoveScreen> createState() => _PeopleLoveScreenState();
}

class _PeopleLoveScreenState extends State<PeopleLoveScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        centerTitle: true,
        title: Text(
          'People You\nLoved',
          textAlign: TextAlign.center,
          style: getWhiteTextStyle(
              fontWeight: FontWeightManager.semiBold,
              fontSize: FontSizeManager.f20),
        ),
        actions: [
          IconButton(
            onPressed: () {},
            icon: const Icon(
              Icons.search,
              size: AppSize.s30,
            ),
          ),
        ],
      ),
      body: Column(
        children: [
          const SizedBox(
            height: AppSize.s50,
          ),
          Expanded(
            child: ListView.builder(
              itemBuilder: (context, index) {
                return const PeopleLoveCardWidget();
              },
              itemCount: 10,
            ),
          ),
        ],
      ),
    );
  }
}
