#!/usr/bin/env python3

import os
import rospy
from std_msgs.msg import String
import openai

def callback_gpt_input(msg):
    """
    Callback that fires whenever a message appears on /gpt_input.
    It sends the text prompt to ChatGPT and publishes the response
    to /gpt_output.
    """
    user_input = msg.data
    rospy.loginfo("ROSGPT: Received input: %s", user_input)

    # Get the ChatGPT response
    response_text = query_openai_chatgpt(user_input)

    # Publish the response
    pub_gpt_output.publish(response_text)
    rospy.loginfo("ROSGPT: Published response: %s", response_text)


def query_openai_chatgpt(prompt):
    """
    Sends the prompt to the OpenAI ChatGPT API
    and returns the generated response text.
    """
    try:
        # Example usage for GPT-3.5
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.7,
        )
        # Extract text from the response
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        rospy.logerr("Error calling OpenAI API: %s", str(e))
        return "Error: Could not retrieve response from OpenAI."


if __name__ == "__main__":
    # 1. Initialize the ROS node
    rospy.init_node("rosgpt_node")

    # 2. Retrieve the OpenAI API Key
    openai_api_key = os.environ.get('OPENAI_API_KEY')
    if not openai_api_key:
        rospy.logerr("OPENAI_API_KEY not found in the environment.")
        rospy.signal_shutdown("No OpenAI API Key provided.")
        exit(1)
    else:
        openai.api_key = openai_api_key

    # 3. Create a publisher for /gpt_output
    pub_gpt_output = rospy.Publisher("/gpt_output", String, queue_size=10)

    # 4. Subscribe to /gpt_input
    rospy.Subscriber("/gpt_input", String, callback_gpt_input)

    # 5. Keep the node running
    rospy.loginfo("ROSGPT: Node started. Awaiting input on /gpt_input.")
    rospy.spin() 