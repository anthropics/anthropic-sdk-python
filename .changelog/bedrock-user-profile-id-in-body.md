fix(bedrock): send the user profile ID in the request body

Amazon Bedrock reads `user_profile_id` from the request body and ignores the `anthropic-user-profile-id` header, so a profile ID given to `AnthropicBedrock` or `AsyncAnthropicBedrock` was not applied. Both clients now move it into the body of Messages requests and no longer send the header. A `user_profile_id` already in the body takes priority over the header.

Some models on Bedrock do not support user profiles. A request to one of them with a profile ID now fails with a 400 error; before, the ID was ignored. Leave the ID off requests to those models.
