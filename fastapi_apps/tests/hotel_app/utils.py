query_items = """
                hotelReview {
                numOfReviews
                ratingOutOf10
                comfortRatingOutOf10
                cleanlinessRatingOutOf10
                facilitiesRatingOutOf10
                freeWifiRatingOutOf10
                hotelId
                id
                locationRatingOutOf10
                staffRatingOutOf10
                subjectiveRating
                valueForMoneyRatingOutOf10
                }
                amenities
                description
                hotelGuestReviews {
                date
                hotelId
                id
                negative
                positive
                title
                }
                hotelHouseRules {
                ageRestriction
                cancellationPayment
                cardsAccepted
                checkIn
                checkOut
                childrenBeds
                groups
                hotelId
                id
                pets
                refundableDamageDeposit
                smoking
                }
                hotelLocation {
                address
                city
                hotelId
                id
                }
                hotelRooms {
                guestCount
                guestCountNumeric
                hotelId
                id
                price
                priceNumeric
                roomType
                taxAndFeeNumeric
                }
                id
                imageLink
                title
            """
