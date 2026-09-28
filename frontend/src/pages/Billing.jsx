import { useEffect, useState } from "react";
import {
    CreditCard,
    FileText,
    Loader2,
} from "lucide-react";

import { getBillingHistory } from "../api/billingApi";

import "./Billing.css";

const Billing = () => {
    const [billingHistory, setBillingHistory] =
        useState([]);

    const [loading, setLoading] =
        useState(true);

    const [error, setError] =
        useState("");

    useEffect(() => {
        loadBillingHistory();
    }, []);

    const loadBillingHistory = async () => {
        try {
            setLoading(true);
            setError("");

            const data =
                await getBillingHistory();

            setBillingHistory(data);
        } catch (error) {
            console.error(
                "Failed to load billing history:",
                error
            );

            setError(
                error.response?.data?.detail ||
                "Failed to load billing history"
            );
        } finally {
            setLoading(false);
        }
    };

    const formatDate = (date) => {
        if (!date) {
            return "-";
        }

        return new Date(
            date
        ).toLocaleString();
    };

    const formatAmount = (amount) => {
        if (amount === null || amount === undefined) {
            return "₹0.00";
        }

        return `₹${Number(amount).toFixed(2)}`;
    };

    if (loading) {
        return (
            <div className="billing-loading">
                <Loader2
                    size={24}
                    className="billing-spinner"
                />

                Loading billing history...
            </div>
        );
    }

    return (
        <div className="billing-page">

            {/* HEADER */}

            <div className="billing-header">
                <div>
                    <h1>Billing</h1>

                    <p>
                        View your subscription
                        billing history
                    </p>
                </div>

                <CreditCard size={32} />
            </div>

            {/* ERROR */}

            {error && (
                <div className="billing-error">
                    {error}
                </div>
            )}

            {/* EMPTY */}

            {!error &&
                billingHistory.length === 0 && (
                    <div className="billing-empty">
                        <FileText size={42} />

                        <h3>
                            No billing history
                        </h3>

                        <p>
                            Your subscription
                            payments will appear
                            here.
                        </p>
                    </div>
                )}

            {/* BILLING TABLE */}

            {!error &&
                billingHistory.length > 0 && (
                    <div className="billing-card">

                        <div className="billing-table-wrapper">

                            <table className="billing-table">

                                <thead>
                                    <tr>
                                        <th>
                                            Transaction ID
                                        </th>

                                        <th>
                                            Plan
                                        </th>

                                        <th>
                                            Amount
                                        </th>

                                        <th>
                                            Billing Date
                                        </th>

                                        <th>
                                            Status
                                        </th>

                                        <th>
                                            Invoice
                                        </th>
                                    </tr>
                                </thead>

                                <tbody>
                                    {billingHistory.map(
                                        (billing) => (
                                            <tr
                                                key={
                                                    billing.id
                                                }
                                            >
                                                <td>
                                                    <span className="transaction-id">
                                                        {
                                                            billing.transaction_id
                                                        }
                                                    </span>
                                                </td>

                                                <td>
                                                    Plan #
                                                    {
                                                        billing.plan_id
                                                    }
                                                </td>

                                                <td className="billing-amount">
                                                    {formatAmount(
                                                        billing.amount
                                                    )}
                                                </td>

                                                <td>
                                                    {formatDate(
                                                        billing.billing_date
                                                    )}
                                                </td>

                                                <td>
                                                    <span
                                                        className={`payment-status ${
                                                            billing.payment_status
                                                                ?.toLowerCase()
                                                                ===
                                                            "success"
                                                                ? "status-success"
                                                                : "status-other"
                                                        }`}
                                                    >
                                                        {
                                                            billing.payment_status
                                                        }
                                                    </span>
                                                </td>

                                                <td>
                                                    {billing.invoice_path ? (
                                                        <a
                                                            href={
                                                                billing.invoice_path
                                                            }
                                                            target="_blank"
                                                            rel="noreferrer"
                                                            className="invoice-link"
                                                        >
                                                            <FileText
                                                                size={
                                                                    15
                                                                }
                                                            />

                                                            View
                                                        </a>
                                                    ) : (
                                                        <span className="no-invoice">
                                                            -
                                                        </span>
                                                    )}
                                                </td>
                                            </tr>
                                        )
                                    )}
                                </tbody>

                            </table>

                        </div>

                    </div>
                )}

        </div>
    );
};

export default Billing;