from flask import Flask, render_template, request, session, redirect, url_for
from markupsafe import Markup
import markdown 
from dotenv import load_dotenv
from app.components.retriever import create_qa_chain
import os


load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")


app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/", methods=["GET", "POST"])
def index():
    """Main route for chatbot interaction."""

    if "messages" not in session:
        session["messages"] = []

    if request.method == "POST":
        user_input = request.form.get("prompt", "").strip()

        if user_input:
            ## Append user message
            messages = session["messages"]
            messages.append({"role": "user", "content": user_input})

            try:
                ## Create QA chain and generate raw response
                qa_chain = create_qa_chain()
                result = qa_chain(user_input)

                ## Extract raw response text
                if isinstance(result, dict) and "result" in result:
                    raw_assistant_reply = result["result"]
                else:
                    raw_assistant_reply = str(result)

                ## Convert RAW Markdown output to HTML
                html_assistant_reply = str(Markup(markdown.markdown(raw_assistant_reply)))

                ## Append HTML-formatted assistant message
                messages.append({"role": "assistant", "content": html_assistant_reply})
                session["messages"] = messages ## Update session with new messages

            except Exception as e:
                print(f"Error during QA chain execution: {e}")
                error_msg = f"An error occurred while processing your request. Please check the server logs."
                return render_template(
                    "index.html",
                    messages=session["messages"],
                    error=error_msg,
                )

        ## Redirect to clear POST form and show updated chat
        return redirect(url_for("index"))

    ## Render chat history
    return render_template("index.html", messages=session.get("messages", []))


@app.route("/clear")
def clear():
    """Clears the chat history from the session."""
    session.pop("messages", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8012,
        debug=False,
        use_reloader=False,
    )