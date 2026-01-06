# main.py
import sys
from interview_simulator.workflows.graph import create_graph

# Main function
def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_resume.pdf>")
        sys.exit(1)

    resume_path = sys.argv[1]
    # Get Job Description from user
    print("\nPaste the full Job Description below:")
    print("(When finished, press Ctrl+D on Mac/Linux or Ctrl+Z + Enter on Windows)\n")

    jd_lines = []
    try:
        while True:
            line = input()
            jd_lines.append(line)
    except EOFError:
        pass

    jd_text = "\n".join(jd_lines).strip()

    if not jd_text:
        print("Error: No job description provided.")
        sys.exit(1)

    app = create_graph()

    config = {"configurable": {"thread_id": "local_session_1"}}

    inputs = {
        "resume_path": resume_path,
        "jd_text": jd_text,
        "current_question_num": 0,
        "max_questions": 5,
        "interview_history": []
    }

    print("\n" + "="*60)
    print("STARTING AI INTERVIEW SIMULATOR")
    print("="*60)
    print("Analyzing resume and JD...\n")

    profile_printed = False  

    for step in app.stream(inputs, config, stream_mode="values"):
        # Print profile ONLY ONCE, the first time it's available
        if not profile_printed and "profile" in step and step["profile"]:
            print("\nCANDIDATE PROFILE")
            print("-" * 40)
            print(step["profile"].model_dump_json(indent=2))
            print("\nStarting interview...\n")
            profile_printed = True

        # Final evaluation (only at the end)
        if "evaluation" in step and step.get("evaluation"):
            eval_result = step["evaluation"]
            print("\n" + "="*60)
            print("FINAL EVALUATION RESULTS")
            print("="*60)
            print(eval_result.summary)
            print(f"\nOverall Score: {eval_result.overall_score:.1f}/10\n")

            for i, q_eval in enumerate(eval_result.evaluations, 1):
                print(f"Question {i} → {q_eval.score:.1f}/10")
                if q_eval.strengths:
                    print(" Strengths: \n", " | ".join(q_eval.strengths))
                if q_eval.weaknesses:
                    print(" Weaknesses: \n", " | ".join(q_eval.weaknesses))
                if q_eval.feedback:
                    print(" Feedback: \n", q_eval.feedback)
                if q_eval.areas_to_improve:
                    print(" **Areas to Improve:** \n", " | ".join(q_eval.areas_to_improve))
                print()


            print("Interview completed successfully!")
            break  
if __name__ == "__main__":
    main()