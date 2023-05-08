import 'package:flutter/material.dart';
import 'package:tender_app_windy/src/theme_manager/asset_image_icon_manager.dart';
import 'package:tender_app_windy/src/theme_manager/font_manager.dart';
import 'package:tender_app_windy/src/theme_manager/style_manager.dart';
import 'package:tender_app_windy/src/theme_manager/values_manager.dart';

class GlassCardWidget extends StatelessWidget {
  const GlassCardWidget({
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      height: 80,
      padding: const EdgeInsetsDirectional.symmetric(
          vertical: AppPadding.p15, horizontal: AppPadding.p24),
      margin: const EdgeInsets.symmetric(
          vertical: AppMargin.m26, horizontal: AppMargin.m30),
      decoration: const BoxDecoration(
        image: DecorationImage(
          fit: BoxFit.cover,
          image: AssetImage(
              '${AssetImageIconManager.assetPath}/glass_card_image.png'),
        ),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Sabrina',
                style: getWhiteTextStyle(
                  fontSize: FontSizeManager.f20,
                  fontWeight: FontWeightManager.semiBold,
                ),
              ),
              Text(
                '22, Traveler',
                style: getWhiteTextStyle(
                  fontSize: FontSizeManager.f14,
                ),
              ),
            ],
          ),
          Container(
            width: 50.0,
            height: 50.0,
            decoration: const BoxDecoration(
                image: DecorationImage(
                    image: AssetImage(
                        '${AssetImageIconManager.assetPath}/icon_profile.png'))),
          )
        ],
      ),
    );
  }
}
