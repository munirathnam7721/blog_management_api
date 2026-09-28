import { useState } from "react";

import {
    Send,
    Bot,
    User,
    Loader2,
} from "lucide-react";

import { sendAIMessage } from "../api/aiSupportApi";
import "./AISupport.css";

const AISupport = () => {

    const [message, setMessage] = useState("");

    const [messages, setMessages] = useState([]);

    const [loading, setLoading] = useState(false);

    const [error, setError] = useState("");


    // ==========================================
    // SEND MESSAGE
    // ==========================================

    const handleSubmit = async (event) => {

        event.preventDefault();

        const trimmedMessage =
            message.trim();

        if (!trimmedMessage) {
            return;
        }

        // Add user's message immediately
        setMessages((previousMessages) => [
            ...previousMessages,
            {
                type: "user",
                text: trimmedMessage,
            },
        ]);

        setMessage("");

        setError("");

        setLoading(true);


        try {

            const response =
                await sendAIMessage(
                    trimmedMessage
                );


            // Add AI response
            setMessages(
                (previousMessages) => [
                    ...previousMessages,
                    {
                        type: "ai",
                        text: response.ai_response,
                    },
                ]
            );

        } catch (error) {

            console.error(
                "AI Support error:",
                error
            );

            const detail =
                error.response?.data?.detail;

            if (
                typeof detail === "string"
            ) {

                setError(detail);

            } else {

                setError(
                    "Unable to get a response from AI Support."
                );

            }

        } finally {

            setLoading(false);

        }
    };


    // ==========================================
    // CLEAR CHAT
    // ==========================================

    const handleClearChat = () => {

        setMessages([]);

        setError("");

    };


    return (
        <div className="ai-support-page">

            {/* ================================= */}
            {/* HEADER */}
            {/* ================================= */}

            <div className="ai-support-header">

                <div>

                    <h1>
                        AI Support
                    </h1>

                    <p>
                        Ask questions about your
                        blog management system.
                    </p>

                </div>


                {messages.length > 0 && (

                    <button
                        type="button"
                        className="clear-chat-button"
                        onClick={handleClearChat}
                    >
                        Clear Chat
                    </button>

                )}

            </div>


            {/* ================================= */}
            {/* CHAT AREA */}
            {/* ================================= */}

            <div className="ai-chat-container">

                {/* Welcome message */}

                {messages.length === 0 && (

                    <div className="ai-welcome">

                        <div className="ai-welcome-icon">

                            <Bot size={32} />

                        </div>

                        <h2>
                            How can I help you?
                        </h2>

                        <p>
                            Ask me about posts,
                            subscriptions, comments,
                            likes, notifications,
                            dashboard, or your account.
                        </p>


                        <div className="ai-example-questions">

                            <button
                                type="button"
                                onClick={() =>
                                    setMessage(
                                        "How can I create a post?"
                                    )
                                }
                            >
                                How can I create a post?
                            </button>

                            <button
                                type="button"
                                onClick={() =>
                                    setMessage(
                                        "How can I edit a post?"
                                    )
                                }
                            >
                                How can I edit a post?
                            </button>

                            <button
                                type="button"
                                onClick={() =>
                                    setMessage(
                                        "How can I check my notifications?"
                                    )
                                }
                            >
                                How can I check my notifications?
                            </button>

                            <button
                                type="button"
                                onClick={() =>
                                    setMessage(
                                        "How can I manage my subscription?"
                                    )
                                }
                            >
                                How can I manage my subscription?
                            </button>

                        </div>

                    </div>

                )}


                {/* ================================= */}
                {/* MESSAGES */}
                {/* ================================= */}

                {messages.length > 0 && (

                    <div className="ai-messages">

                        {messages.map(
                            (item, index) => (

                                <div
                                    key={index}
                                    className={
                                        item.type === "user"
                                            ? "ai-message user-message"
                                            : "ai-message bot-message"
                                    }
                                >

                                    <div className="message-icon">

                                        {item.type === "user" ? (
                                            <User size={18} />
                                        ) : (
                                            <Bot size={18} />
                                        )}

                                    </div>


                                    <div className="message-content">

                                        <div className="message-label">

                                            {item.type === "user"
                                                ? "You"
                                                : "AI Support"
                                            }

                                        </div>

                                        <p>
                                            {item.text}
                                        </p>

                                    </div>

                                </div>

                            )
                        )}


                        {/* Loading */}

                        {loading && (

                            <div className="ai-message bot-message">

                                <div className="message-icon">

                                    <Bot size={18} />

                                </div>

                                <div className="message-content">

                                    <div className="message-label">
                                        AI Support
                                    </div>

                                    <div className="ai-loading">

                                        <Loader2
                                            size={18}
                                            className="loading-icon"
                                        />

                                        Thinking...

                                    </div>

                                </div>

                            </div>

                        )}

                    </div>

                )}


                {/* ================================= */}
                {/* ERROR */}
                {/* ================================= */}

                {error && (

                    <div className="ai-error">

                        {error}

                    </div>

                )}


                {/* ================================= */}
                {/* INPUT */}
                {/* ================================= */}

                <form
                    onSubmit={handleSubmit}
                    className="ai-input-form"
                >

                    <input
                        type="text"
                        value={message}
                        onChange={(event) =>
                            setMessage(
                                event.target.value
                            )
                        }
                        placeholder="Ask AI Support..."
                        disabled={loading}
                    />


                    <button
                        type="submit"
                        disabled={
                            loading ||
                            !message.trim()
                        }
                    >

                        {loading ? (
                            <Loader2
                                size={18}
                                className="loading-icon"
                            />
                        ) : (
                            <Send size={18} />
                        )}

                        Send

                    </button>

                </form>

            </div>

        </div>
    );
};


export default AISupport;