import requests
import json
import time
import ast
import re
from argparse import ArgumentParser
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import utc
from datetime import timedelta, date

#PATH = "C:\Users\nilanjan.das\Downloads"
parser = ArgumentParser(description='finds the number of *full* calendar weeks between 2 dates')
parser.add_argument("--o_path", type = str,  help="output path of downlodable file")
opt = parser.parse_args()
class reportgenerators():

    def __init__(self):
        pass

    ## generate the access token with refresh token ##

    def accesstoken(self):
        url = "https://api.amazon.com/auth/o2/token"

        payload = 'grant_type=refresh_token&refresh_token=Atzr%7CIwEBIKdJMvhPsgbuh-LiUcZfBhCBNsQl0Q1gXwT_PnIiuZj8P2MRQogJE4mkKOqNAj_6fK9mOuxpNUFr7VReUtM_OdAP4499FBLQ4U-_s49a9zvz9hDTR6etehbe8O8ciMZlsoGMXClhQ_W3HnBg11Rb5-vbpfRuoA0vq0xauaHdkjvOGiMiBZHhfaDU1eD8nxwj-UEgviVn-7IvH2_yAVO6CbEL2RcYUDTcu1750OVl4MSj_HXUHKICim263y3oGpmQgGKmVIAX6ql1r-d1xFL9IzLMxRcWqXoPrIMzlR7VwMXGGMO8L0BMQtEpoOzYSHxEP_wu06zW_tlN0kuqV4veHV56JHzdnBKfi_wG6XAesSfj2guX6bZ1FbqX9xDqLLQgZp2nT8g9nuf7brXIDwfG4MUAh-GhRHppEyNqelU0XhfnAiMuRLkis5je3sHjLyeXL3DGFLmZk-oFO3anBeOiXkwQ&client_id=amzn1.application-oa2-client.ec2691f7016249168bc71bd8dd0677c8&client_secret=b523500dc9d7afe1ebb0eebe43d3fd8fccdf3f7e062ba738dc2989d438abb242'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data=payload, timeout=5)

        person_dict = json.loads(response.text)
        print("Access token is successfully generated")
        return person_dict['access_token']

    ## generate the profile ids ##########

    def proflIds(self, acs_token, client_id):

        url = "https://advertising-api-eu.amazon.com/v2/profiles"
        agency_profile = []
        payload = ""
        headers = {
            'Content-Type': 'application/json',
            'Amazon-Advertising-API-ClientId': client_id,
            'Authorization': acs_token
        }

        response = requests.request("GET", url, headers=headers, data=payload, timeout=5)

        json_par = json.loads(response.text)
        # print(response.text)

        for i in json_par:
            if i['accountInfo']['type'] == 'agency':
                agency_profile.append(i['profileId'])

        print("Profile ids are successfully generated")

        return agency_profile

    ####### request reports ######

    def req_Report(self, agncy_ids, acs_token, client_id,start,end):

        url = "https://advertising-api-eu.amazon.com/dsp/reports"
        dict_Ids = {}

        for prflid in agncy_ids:
            payload = json.dumps({
                "format": "CSV",
                "metrics": "totalCost, supplyCost, amazonAudienceFee, advertiserTimezone, advertiserCountry, amazonPlatformFee, impressions, clickThroughs, CTR, eCPM, eCPC, dpv14d, dpvViews14d, dpvClicks14d,dpvr14d, eCPDPV14d, pRPV14d, pRPVViews14d, pRPVClicks14d, pRPVr14d, eCPPRPV14d, atl14d, atlViews14d, atlClicks14d, atlr14d, eCPAtl14d, atc14d, atcViews14d, atcClicks14d, atcr14d, eCPAtc14d, purchases14d, purchasesViews14d, purchasesClicks14d, purchaseRate14d, eCPP14d, newToBrandPurchases14d, newToBrandPurchasesViews14d, newToBrandPurchasesClicks14d, newToBrandPurchaseRate14d, newToBrandECPP14d, percentOfPurchasesNewToBrand14d, addToWatchlist14d, addToWatchlistViews14d, addToWatchlistClicks14d, addToWatchlistCVR14d, addToWatchlistCPA14d, downloadedVideoPlays14d, downloadedVideoPlaysViews14d, downloadedVideoPlaysClicks14d, downloadedVideoPlayRate14d, eCPDVP14d, videoStreams14d, videoStreamsViews14d, videoStreamsClicks14d, videoStreamsRate14d, eCPVS14d, playTrailers14d, playTrailersViews14d, playerTrailersClicks14d, playTrailerRate14d, eCPPT14d, rentals14d, rentalsViews14d, rentalsClicks14d, rentalRate14d, ecpr14d, videoDownloads14d, videoDownloadsViews14d, videoDownloadsClicks14d, videoDownloadRate14d, ecpvd14d, newSubscribeAndSave14d, newSubscribeAndSaveViews14d, newSubscribeAndSaveClicks14d, newSubscribeAndSaveRate14d, eCPnewSubscribeAndSave14d, totalPixel14d, totalPixelViews14d, totalPixelClicks14d, totalPixelCVR14d, totalPixelCPA14d, marketingLandingPage14d, marketingLandingPageViews14d, marketingLandingPageClicks14d, marketingLandingPageCVR14d, marketingLandingPageCPA14d, subscriptionPage14d, subscriptionPageViews14d, subscriptionPageClicks14d, subscriptionPageCVR14d, subscriptionPageCPA14d, signUpPage14d, signUpPageViews14d, signUpPageClicks14d, signUpPageCVR14d, signUpPageCPA14d, application14d, applicationViews14d, applicationClicks14d, applicationCVR14d, applicationCPA14d, gameLoad14d, gameLoadViews14d, gameLoadClicks14d, gameLoadCVR14d, gameLoadCPA14d, widgetLoad14d, widgetLoadViews14d, widgetLoadClicks14d, widgetLoadCVR14d, widgetLoadCPA14d, surveyStart14d, surveyStartViews14d, surveyStartClicks14d, surveyStartCVR14d, surveyStartCPA14d, surveyFinish14d, surveyFinishViews14d, surveyFinishClicks14d, surveyFinishCVR14d, surveyFinishCPA14d, bannerInteraction14d, bannerInteractionViews14d, bannerInteractionClicks14d, bannerInteractionCVR14d, bannerInteractionCPA14d, widgetInteraction14d, widgetInteractionViews14d, widgetInteractionClicks14d, widgetInteractionCVR14d, widgetInteractionCPA14d, gameInteraction14d, gameInteractionViews14d, gameInteractionClicks14d, gameInteractionCVR14d, gameInteractionCPA14d, emailLoad14d, emailLoadViews14d, emailLoadClicks14d, emailLoadCVR14d, emailLoadCPA14d, emailInteraction14d, emailInteractionViews14d, emailInteractionClicks14d, emailInteractionCVR14d, emailInteractionCPA14d, submitButton14d, submitButtonViews14d, submitButtonClicks14d, submitButtonCVR14d, submitButtonCPA14d, purchaseButton14d, purchaseButtonViews14d, purchaseButtonClicks14d, purchaseButtonCVR14d, purchaseButtonCPA14d, clickOnRedirect14d, clickOnRedirectViews14d, clickOnRedirectClicks14d, clickOnRedirectCVR14d, clickOnRedirectCPA14d, signUpButton14d, signUpButtonViews14d, signUpButtonClicks14d, signUpButtonCVR14d, signUpButtonCPA14d, subscriptionButton14d, subscriptionButtonViews14d, subscriptionButtonClicks14d, subscriptionButtonCVR14d, subscriptionButtonCPA14d, successPage14d, successPageViews14d, successPageClicks14d, successPageCVR14d, successPageCPA14d, thankYouPage14d, thankYouPageViews14d, thankYouPageClicks14d, thankYouPageCVR14d, thankYouPageCPA14d, registrationForm14d, registrationFormViews14d, registrationFormClicks14d, registrationFormCVR14d, registrationFormCPA14d, registrationConfirmPage14d, registrationConfirmPageViews14d, registrationConfirmPageClicks14d, registrationConfirmPageCVR14d, registrationConfirmPageCPA14d, storeLocatorPage14d, storeLocatorPageViews14d, storeLocatorPageClicks14d, storeLocatorPageCVR14d, storeLocatorPageCPA14d, mobileAppFirstStarts14d, mobileAppFirstStartViews14d, mobileAppFirstStartClicks14d, mobileAppFirstStartCVR14d, mobileAppFirstStartsCPA14d, brandStoreEngagement1, brandStoreEngagement1Views, brandStoreEngagement1Clicks, brandStoreEngagement1CVR, brandStoreEngagement1CPA, brandStoreEngagement2, brandStoreEngagement2Views, brandStoreEngagement2Clicks, brandStoreEngagement2CVR, brandStoreEngagement2CPA, brandStoreEngagement3, brandStoreEngagement3Views, brandStoreEngagement3Clicks, brandStoreEngagement3CVR, brandStoreEngagement3CPA, brandStoreEngagement4, brandStoreEngagement4Views, brandStoreEngagement4Clicks, brandStoreEngagement4CVR, brandStoreEngagement4CPA, brandStoreEngagement5, brandStoreEngagement5Views, brandStoreEngagement5Clicks, brandStoreEngagement5CVR, brandStoreEngagement5CPA, brandStoreEngagement6, brandStoreEngagement6Views, brandStoreEngagement6Clicks, brandStoreEngagement6CVR, brandStoreEngagement6CPA, brandStoreEngagement7, brandStoreEngagement7Views, brandStoreEngagement7Clicks, brandStoreEngagement7CVR, brandStoreEngagement7CPA, addedToShoppingCart14d, addedToShoppingCartViews14d, addedToShoppingCartClicks14d, addedToShoppingCartCVR14d, addedToShoppingCartCPA14d, productPurchased, productPurchasedViews, productPurchasedClicks, productPurchasedCVR, productPurchasedCPA, homepageVisit14d, homepageVisitViews14d, homepageVisitClicks14d, homepageVisitCVR14d, homepageVisitCPA14d, videoStarted, videoStartedViews, videoStartedClicks, videoStartedCVR, videoStartedCPA, videoCompleted, videoCompletedViews, videoEndClicks, videoCompletedCVR, videoCompletedCPA, messageSent14d, messageSentViews14d, messageSentClicks14d, messageSentCVR14d, messageSentCPA14d, mashupClickToPage, mashupClickToPageViews, mashupClickToPageClicks, mashupClickToPageCVR, mashupClickToPageCPA, mashupBackupImage, mashupBackupImageViews, mashupBackupImageClicks, mashupBackupImageCVR, mashupBackupImageCPA, mashupAddToCart14d, mashupAddToCartViews14d, mashupAddToCartClicks14d, mashupAddToCartClickCVR14d, mashupAddToCartCPA14d, mashupAddToWishlist14d, mashupAddToWishlistViews14d, mashupAddToWishlistClicks14d, mashupAddToWishlistCVR14d, mashupAddToWishlistCPA14d, mashupSubscribeAndSave14d, mashupSubscribeAndSaveClickViews14d, mashupSubscribeAndSaveClick14d, mashupSubscribeAndSaveCVR14d, mashupSubscribeAndSaveCPA14d, mashupClipCouponClick14d, mashupClipCouponClickViews14d, mashupClipCouponClickClicks14d, mashupClipCouponClickCVR14d, mashupClipCouponClickCPA14d, mashupShopNowClick14d, mashupShopNowClickViews14d, mashupShopNowClickClicks14d, mashupShopNowClickCVR14d, mashupShopNowClickCPA14d, referral14d, referralViews14d, referralClicks14d, referralCVR14d, referralCPA14d, accept14d, acceptViews14d, acceptClicks14d, acceptCVR14d, acceptCPA14d, decline14d, declineViews14d, declineClicks14d, declineCVR14d, declineCPA14d, videoStart, videoFirstQuartile, videoMidpoint, videoThirdQuartile, videoComplete, videoCompletionRate, ecpvc, videoPause, videoResume, videoMute, videoUnmute, dropDownSelection14d, dropDownSelectionViews14d, dropDownSelectionClicks14d, dropDownSelectionCVR14d, dropDownSelectionCPA14d, brandSearch14d, brandSearchViews14d, brandSearchClicks14d, brandSearchRate14d, brandSearchCPA14d, grossImpressions, grossClickThroughs, invalidImpressions, invalidClickThroughs, invalidImpressionRate, invalidClickThroughsRate, agencyFee, totalFee, 3pFeeAutomotive, 3pFeeAutomotiveAbsorbed, 3pFeeComScore, 3pFeeComScoreAbsorbed, 3pFeeCPM1, 3pFeeCPM1Absorbed, 3pFeeCPM2, 3pFeeCPM2Absorbed, 3pFeeCPM3, 3pFeeCPM3Absorbed, 3pFeeDoubleclickCampaignManager, 3pFeeDoubleclickCampaignManagerAbsorbed, 3pFeeDoubleVerify, 3pFeeDoubleVerifyAbsorbed, 3pFeeIntegralAdScience, 3pFeeIntegralAdScienceAbsorbed, 3PFees, unitsSold14d, sales14d, ROAS14d, eRPM14d, newToBrandUnitsSold14d, newToBrandProductSales14d, newToBrandROAS14d, newToBrandERPM14d, totalPRPV14d, totalPRPVViews14d, totalPRPVClicks14d, totalPRPVr14d, totalECPPRPV14d, totalPurchases14d, totalPurchasesViews14d, totalPurchasesClicks14d, totalPurchaseRate14d, totalECPP14d, totalNewToBrandPurchases14d, totalNewToBrandPurchasesViews14d, totalNewToBrandPurchasesClicks14d, totalNewToBrandPurchaseRate14d, totalNewToBrandECPP14d, totalPercentOfPurchasesNewToBrand14d, totalUnitsSold14d, totalSales14d, totalROAS14d, totalERPM14d, totalNewToBrandUnitsSold14d, totalNewToBrandProductSales14d, totalNewToBrandROAS14d, totalNewToBrandERPM14d, viewableImpressions, measurableImpressions, measurableRate, viewabilityRate, totalDetailPageViews14d, totalDetailPageViewViews14d, totalDetailPageClicks14d, totalDetailPageViewsCVR14d, totalDetaiPageViewCPA14d, totalAddToList14d, totalAddToListViews14d, totalAddToListClicks14d, totalAddToListCVR14d, totalAddToListCPA14d, totalAddToCart14d, totalAddToCartViews14d, totalAddToCartClicks14d, totalAddToCartCVR14d, totalAddToCartCPA14d, totalSubscribeAndSaveSubscriptions14d, totalSubscribeAndSaveSubscriptionViews14d, totalSubscribeAndSaveSubscriptionClicks14d, totalSubscribeAndSaveSubscriptionCVR14d, totalSubscribeAndSaveSubscriptionCPA14d",
                "type": "CAMPAIGN",
                "dimensions": [
                    "ORDER",
                    "LINE_ITEM",
                    "CREATIVE"
                ],
                "timeUnit": "DAILY",
                "startDate": start,
                "endDate": end
            })
            headers = {
                'Amazon-Advertising-API-Scope': str(prflid),
                'Content-Type': 'application/json',
                'Amazon-Advertising-API-ClientId': client_id,
                'Authorization': acs_token
            }

            response = requests.request("POST", url, headers=headers, data=payload, timeout=10)

            # print(response.text)

            id_par = json.loads(response.text)
            reportId = id_par['reportId']
            dict_Ids.update({reportId: str(prflid)})

            print("Reports are requested and report ids generated")
        return dict_Ids

    ### generate reports ####

    def get_Report(self, dict_Ids, acs_token, client_id):

        response_list = []
        for reportId, prflid in dict_Ids.items():

            url = "https://advertising-api-eu.amazon.com/dsp/reports/%s" % reportId

            payload = ""
            headers = {
                'Amazon-Advertising-API-Scope': prflid,
                'Content-Type': 'application/json',
                'Amazon-Advertising-API-ClientId': client_id,
                'Authorization': acs_token
            }
            time.sleep(5)
            response = requests.request("GET", url, headers=headers, data=payload, timeout=5)
            # print(response.text)
            latest_response = ast.literal_eval(response.text)
            print(latest_response)

            ######## wait until a report successfully generated ##########

            if latest_response['status'] == True:

                if latest_response['status'] == 'IN_PROGRESS':
                    for i in range(0, 100, 1):
                        time.sleep(5)
                        response = requests.request("GET", url, headers=headers, data=payload, timeout=5)
                        latest_response = ast.literal_eval(response.text)
                        if latest_response['status'] == 'IN_PROGRESS':
                            continue

                        else:
                            break
                elif latest_response['status'] == 'FAILURE':
                    print("The respose is a failure Failure")
                else:
                    pass
                break
            else:
                pass

            if len(latest_response["location"]) > 0 and latest_response["status"] == "SUCCESS":
                response_list.append(latest_response["location"])
                print("location is:" + latest_response["location"])
                respons = requests.get(latest_response["location"], timeout=5)
                print("the response is:" + str(respons))
                re1 = '([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))'
                re2 = '(\w+)(\.\w+)+(?!.*(\w+)(\.\w+)+)'
                generic_re = re.compile("(%s|%s)" % (re1, re2)).findall(latest_response["location"])

                # print("date is: "+ (generic_re[0][0] + generic_re[1][0]))

                f_name = generic_re[0][0] + generic_re[1][0]
                print("The file name is:" + f_name)
                open(opt.o_path+ "\\" + f_name, "wb").write(respons.content)
            elif "errors" in latest_response:
                print(latest_response)
            else:
                pass

            print("Report locations are:")
        return response_list

    def call_all_func(self) -> object:

        client_id = 'amzn1.application-oa2-client.ec2691f7016249168bc71bd8dd0677c8'
        end = date.today()
        start = end - timedelta(days=29)
        end= end.strftime("%Y%m%d")
        start= start.strftime("%Y%m%d")
        acs_token = self.accesstoken()
        agncy_ids = self.proflIds(acs_token, client_id)
        dict_Ids = self.req_Report(agncy_ids, acs_token, client_id,start,end)
        response = self.get_Report(dict_Ids, acs_token, client_id)
        # print(response)
        return agncy_ids

    ## main function #######

    # generator = report_Generator()
    # schedule.every(2).minutes.do(generator)


if __name__ == '__main__':

    obj = reportgenerators()
    profiles = obj.call_all_func()
    sched = BackgroundScheduler(timezone=utc)
    sched.add_job(obj.call_all_func, 'interval', seconds=180, max_instances=len(profiles))
    sched.start()
    while True:
        time.sleep(1)