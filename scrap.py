import openai
import pandas as pd

openai.api_key = "sk-None-zSwLA9mo3oKXeQIxyfDiT3BlbkFJ7jUS3aRcElyRcVPGsXRJ"

def categorize_competitor(competitor_data):
    """
    Sends a prompt to the GPT model to categorize a competitor's services,
    handling potential API errors and empty responses.

    Args:
        competitor_data (dict): A dictionary containing competitor information.

    Returns:
        str (or None): The predicted category or None if an error occurs.
    """
    prompt = f"This competitor, {competitor_data['Name']}, offers services including {competitor_data['Description']}. What category of services does this competitor most likely fall under (e.g., bulk email sending, MTA management, email delivery optimization)?"

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Adjust engine as needed
            prompt=prompt,
            max_tokens=100,  # Adjust maximum response length if needed
            n=1,
            stop=None,
            temperature=0.7  # Adjust temperature for creativity vs. accuracy
        )
        if response.choices and response.choices[0].text:
            return response.choices[0].text.strip().split("\n")[-1]
        else:
            return None  # Indicate error or empty response

    except openai.error.OpenAIError as e:
        print(f"Error categorizing competitor: {e}")
        return None

def main():
    # Load competitor data from CSV file (adjust path and columns)
    try:
        df = pd.read_csv("/mnt/data/Find-Companies-Table-(17-July-2024)-Default-View-export-1721205032800.csv")
    except FileNotFoundError:
        print("Error: Competitor CSV file not found. Please check the path.")
        return

    # Apply the categorization function to each row
    df["Category"] = df.apply(lambda row: categorize_competitor(row.to_dict()), axis=1)

    # Filter competitors based on category (optional)
    filtered_df = df[df["Category"].isin(["bulk email sending", "MTA management", "email delivery optimization"])]

    # Print or save the categorized and (optionally) filtered data
    print(df.to_string())  # Print all data
    filtered_df.to_csv("/mnt/data/categorized_competitors.csv", index=False)  # Save filtered data

if __name__ == "_main_":
    main()
