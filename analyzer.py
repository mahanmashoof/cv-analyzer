import os
import sys
import argparse
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def analyze_cv(cv_text: str, job_description: str) -> str:
    prompt = f"""You are a senior technical recruiter and career coach.

Analyze the fit between this CV and job description. Respond with:

1. FIT SCORE: A score from 1-10
2. STRENGTHS: Top 3 reasons this person is a strong candidate
3. GAPS: Top 3 things missing or that could be stronger  
4. KEYWORDS: 5 keywords from the job description present in the CV
5. VERDICT: One sentence summary

Be specific and reference actual details from both texts.

--- CV ---
{cv_text}

--- JOB DESCRIPTION ---
{job_description}
"""
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1200,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text

def main():
    # Set up the argument parser — defines what flags the CLI accepts
    parser = argparse.ArgumentParser(
        description="Analyze your CV against a job description using Claude"
    )
    parser.add_argument(
        "--job",
        type=str,
        help="Job description text (paste it in quotes)",
        required=False
    )
    parser.add_argument(
        "--job-file",
        type=str,
        help="Path to a .txt file containing the job description",
        required=False
    )
    parser.add_argument(
        "--cv",
        type=str,
        default="cv.txt",
        help="Path to your CV file (default: cv.txt)"
    )

    args = parser.parse_args()

    # Validate: user must provide either --job or --job-file
    if not args.job and not args.job_file:
        print("Error: provide a job description with --job or --job-file")
        sys.exit(1)   # exit with error code, like process.exit(1) in Node

    # Read inputs
    cv_text = read_file(args.cv)
    job_text = args.job if args.job else read_file(args.job_file)

    print("\n--- CV Analyzer powered by Claude ---\n")
    print("Analyzing fit...\n")

    result = analyze_cv(cv_text, job_text)
    print(result)
    print("\n--- Done ---\n")

# This is Python's equivalent of `if (require.main === module)` in Node
# It means: only run main() if this file is executed directly, not imported
if __name__ == "__main__":
    main()