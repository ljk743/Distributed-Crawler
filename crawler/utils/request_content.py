import json


def comments_request_form_booking(hotel_id, ufi, hotel_country_code, skip):
    url = "https://www.booking.com/dml/graphql"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/126.0.0.0 Safari/537.36",
        "Content-Type": "application/json"
    }
    payload = {
        "operationName": "ReviewList",
        "variables": {
            "input": {
                "hotelId": hotel_id,
                "ufi": ufi,
                "hotelCountryCode": hotel_country_code,
                "sorter": "MOST_RELEVANT",
                "filters": {
                    "text": "",
                    "languages": ["en"]
                },
                "skip": skip,
                "limit": 10,
                "upsortReviewUrl": "",
                "searchFeatures": {
                    "destId": ufi,
                    "destType": "CITY"
                }
            }
        },
        "extensions": {},
        "query": """
                query ReviewList($input: ReviewListFrontendInput!) {
                    reviewListFrontend(input: $input) {
                        ... on ReviewListFrontendResult {
                            ratingScores {
                                name
                                translation
                                value
                                ufiScoresAverage {
                                    ufiScoreLowerBound
                                    ufiScoreHigherBound
                                    __typename
                                }
                                __typename
                            }
                            topicFilters {
                                id
                                name
                                isSelected
                                translation {
                                    id
                                    name
                                    __typename
                                }
                                __typename
                            }
                            reviewScoreFilter {
                                name
                                value
                                count
                                __typename
                            }
                            languageFilter {
                                name
                                value
                                count
                                countryFlag
                                __typename
                            }
                            timeOfYearFilter {
                                name
                                value
                                count
                                __typename
                            }
                            customerTypeFilter {
                                count
                                name
                                value
                                __typename
                            }
                            reviewCard {
                                reviewUrl
                                guestDetails {
                                    username
                                    avatarUrl
                                    countryCode
                                    countryName
                                    avatarColor
                                    showCountryFlag
                                    anonymous
                                    guestTypeTranslation
                                    __typename
                                }
                                bookingDetails {
                                    customerType
                                    roomId
                                    roomType {
                                        id
                                        name
                                        __typename
                                    }
                                    checkoutDate
                                    checkinDate
                                    numNights
                                    __typename
                                }
                                reviewedDate
                                isReviewerChoice
                                isTranslatable
                                helpfulVotesCount
                                reviewScore
                                textDetails {
                                    title
                                    positiveText
                                    negativeText
                                    textTrivialFlag
                                    lang
                                    __typename
                                }
                                isApproved
                                partnerReply {
                                    reply
                                    __typename
                                }
                                positiveHighlights {
                                    start
                                    end
                                    __typename
                                }
                                negativeHighlights {
                                    start
                                    end
                                    __typename
                                }
                                uvcUrl
                                editUrl
                                photos {
                                    id
                                    urls {
                                        size
                                        url
                                        __typename
                                    }
                                    kind
                                    __typename
                                }
                                __typename
                            }
                            reviewsCount
                            sorters {
                                name
                                value
                                __typename
                            }
                            __typename
                        }
                        ... on ReviewsFrontendError {
                            statusCode
                            message
                            __typename
                        }
                        __typename
                    }
                }
                """
    }
    config = [url, headers, payload]
    return config


def comment_request_from_airbnb(str_id, offset):
    url = "https://www.airbnb.co.uk/api/v3/StaysPdpReviewsQuery/dec1c8061483e78373602047450322fd474e79ba9afa8d3dbbc27f504030f91d"
    headers = {
        "X-Airbnb-Api-Key": "d306zoyjsyarp7ifhu67rjxn52tv0t20",
    }

    variables = {
        "id": str_id,
        "pdpReviewsRequest": {
            "fieldSelector": "for_p3_translation_only",
            "forPreview": False,
            "limit": 50,
            "offset": offset,
            "showingTranslationButton": False,
            "first": 50,
            "sortingPreference": "MOST_RECENT",
        }
    }

    extensions = {
        "persistedQuery": {
            "version": 1,
            "sha256Hash": "dec1c8061483e78373602047450322fd474e79ba9afa8d3dbbc27f504030f91d"
        }
    }

    params = {
        "operationName": "StaysPdpReviewsQuery",
        "locale": "en-GB",
        "currency": "GBP",
        "variables": json.dumps(variables),
        "extensions": json.dumps(extensions)
    }

    config = [url, headers, params]
    return config
