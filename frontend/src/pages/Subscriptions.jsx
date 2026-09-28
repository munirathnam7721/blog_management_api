import { useEffect, useState } from "react";
import {
    Check,
    CreditCard,
    Loader2,
    RefreshCw,
} from "lucide-react";
import "./Subscriptions.css";
import {
    getSubscriptionPlans,
    getMySubscription,
    subscribeToPlan,
    renewSubscription,
} from "../api/subscriptionsApi";

const Subscriptions = () => {
    const [plans, setPlans] = useState([]);
    const [subscription, setSubscription] = useState(null);
    const [loading, setLoading] = useState(true);
    const [actionLoading, setActionLoading] =
        useState(false);
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");

    useEffect(() => {
        loadSubscriptionData();
    }, []);

    const loadSubscriptionData = async () => {
        try {
            setLoading(true);
            setError("");

            const [
                plansData,
                subscriptionData,
            ] = await Promise.all([
                getSubscriptionPlans(),
                getMySubscription(),
            ]);

            setPlans(plansData);

            if (
                subscriptionData?.subscription
            ) {
                setSubscription(
                    subscriptionData
                );
            } else {
                setSubscription(null);
            }
        } catch (error) {
            console.error(
                "Failed to load subscription data:",
                error
            );

            setError(
                error.response?.data?.detail ||
                "Failed to load subscription data"
            );
        } finally {
            setLoading(false);
        }
    };

    const handleSubscribe = async (planId) => {
        try {
            setActionLoading(true);
            setError("");
            setSuccess("");

            const response =
                await subscribeToPlan(
                    planId
                );

            setSuccess(
                response.message ||
                "Subscription created successfully"
            );

            await loadSubscriptionData();
        } catch (error) {
            console.error(
                "Subscription error:",
                error
            );

            setError(
                error.response?.data?.detail ||
                "Failed to create subscription"
            );
        } finally {
            setActionLoading(false);
        }
    };

    const handleRenew = async () => {
        try {
            setActionLoading(true);
            setError("");
            setSuccess("");

            const response =
                await renewSubscription();

            setSuccess(
                response.message ||
                "Subscription renewed successfully"
            );

            await loadSubscriptionData();
        } catch (error) {
            console.error(
                "Renewal error:",
                error
            );

            setError(
                error.response?.data?.detail ||
                "Failed to renew subscription"
            );
        } finally {
            setActionLoading(false);
        }
    };

    const formatDate = (date) => {
        if (!date) {
            return "-";
        }

        return new Date(
            date
        ).toLocaleDateString();
    };

    if (loading) {
        return (
            <div className="subscription-loading">
                <Loader2
                    size={24}
                    className="subscription-spinner"
                />

                Loading subscriptions...
            </div>
        );
    }

    return (
        <div className="subscriptions-page">

            <div className="subscriptions-header">
                <div>
                    <h1>
                        Subscriptions
                    </h1>

                    <p>
                        Manage your blog
                        subscription plan
                    </p>
                </div>

                <CreditCard size={32} />
            </div>

            {error && (
                <div className="subscription-error">
                    {error}
                </div>
            )}

            {success && (
                <div className="subscription-success">
                    {success}
                </div>
            )}

            {/* CURRENT SUBSCRIPTION */}

            <section className="current-subscription">

                <h2>
                    Current Subscription
                </h2>

                {subscription ? (
                    <div className="current-subscription-card">

                        <div>
                            <span className="subscription-label">
                                Plan
                            </span>

                            <h3>
                                {
                                    subscription
                                        .plan
                                        ?.name
                                }
                            </h3>
                        </div>

                        <div>
                            <span className="subscription-label">
                                Start Date
                            </span>

                            <p>
                                {formatDate(
                                    subscription
                                        .subscription
                                        ?.start_date
                                )}
                            </p>
                        </div>

                        <div>
                            <span className="subscription-label">
                                End Date
                            </span>

                            <p>
                                {formatDate(
                                    subscription
                                        .subscription
                                        ?.end_date
                                )}
                            </p>
                        </div>

                        <button
                            type="button"
                            className="renew-button"
                            onClick={
                                handleRenew
                            }
                            disabled={
                                actionLoading
                            }
                        >
                            <RefreshCw
                                size={16}
                            />

                            {actionLoading
                                ? "Renewing..."
                                : "Renew"}
                        </button>

                    </div>
                ) : (
                    <div className="no-subscription">
                        <p>
                            You don't have
                            an active
                            subscription.
                        </p>
                    </div>
                )}

            </section>

            {/* AVAILABLE PLANS */}

            <section className="plans-section">

                <h2>
                    Available Plans
                </h2>

                <div className="plans-grid">

                    {plans.map((plan) => (
                        <div
                            className="plan-card"
                            key={plan.id}
                        >

                            <h3>
                                {plan.name}
                            </h3>

                            <div className="plan-price">
                                ₹
                                {plan.price}
                            </div>

                            <p className="plan-description">
                                {
                                    plan.description
                                }
                            </p>

                            <div className="plan-features">

                                <div>
                                    <Check
                                        size={16}
                                    />

                                    <span>
                                        {plan.max_posts ===
                                        null
                                            ? "Unlimited"
                                            : plan.max_posts}{" "}
                                        posts
                                    </span>
                                </div>

                                <div>
                                    <Check
                                        size={16}
                                    />

                                    <span>
                                        {plan.max_images_per_post ===
                                        null
                                            ? "Unlimited"
                                            : plan.max_images_per_post}{" "}
                                        images
                                        per post
                                    </span>
                                </div>

                                <div>
                                    <Check
                                        size={16}
                                    />

                                    <span>
                                        {plan.max_likes ===
                                        null
                                            ? "Unlimited"
                                            : plan.max_likes}{" "}
                                        likes
                                    </span>
                                </div>

                                <div>
                                    <Check
                                        size={16}
                                    />

                                    <span>
                                        {plan.max_comments ===
                                        null
                                            ? "Unlimited"
                                            : plan.max_comments}{" "}
                                        comments
                                    </span>
                                </div>

                            </div>

                            <button
                                type="button"
                                className="subscribe-button"
                                onClick={() =>
                                    handleSubscribe(
                                        plan.id
                                    )
                                }
                                disabled={
                                    actionLoading
                                }
                            >
                                {actionLoading
                                    ? "Processing..."
                                    : "Subscribe"}
                            </button>

                        </div>
                    ))}

                </div>

            </section>

        </div>
    );
};

export default Subscriptions;