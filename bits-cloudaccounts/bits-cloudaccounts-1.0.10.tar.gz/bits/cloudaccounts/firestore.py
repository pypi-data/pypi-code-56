# -*- coding: utf-8 -*-
"""Cloud Accounts Firestore Class file."""

import os

from google.cloud import firestore


class Firestore:
    """Cloud Accounts Firestore Class."""

    def __init__(self, project=None):
        """Initialize a class instance."""
        if not project:
            project = os.environ.get("GCP_PROJECT")
        if not project:
            project = os.environ.get("GOOGLE_CLOUD_PROJECT")
        self.client = firestore.Client(project=project)

    # accounts
    def get_accounts(self):
        """Return a list of Accounts from Firestore."""
        return list(self.client.collection("accounts").stream())

    # actions
    def get_actions(self):
        """Return a list of Actions from Firestore."""
        return list(self.client.collection("actions").stream())

    # amazon accounts
    def get_amazon_account(self, account_name):
        """Return a list of Amazon Accounts from Firestore."""
        return self.client.collection("amazon_accounts").document(account_name).get()

    def get_amazon_accounts(self):
        """Return a list of Amazon Accounts from Firestore."""
        return list(self.client.collection("amazon_accounts").stream())

    # budgets (under google_billing_accounts)
    def get_budget(self, billing_account_name, budget_name):
        """Return a Google Billing Budget from Firestore."""
        ref = self.client.collection("google_billing_accounts").document(billing_account_name)
        return ref.collection("budgets").document(budget_name).get()

    def get_budgets(self, billing_account_name):
        """Return a list of Google Billing Account Budgets from Firestore."""
        ref = self.client.collection("google_billing_accounts").document(billing_account_name)
        return list(ref.collection("budgets").stream())

    # cost objects
    def get_cost_objects(self):
        """Return a list of Cost Objects from Firestore."""
        return list(self.client.collection("cost_objects").stream())

    # google billing accounts
    def get_google_billing_account(self, billing_account_name):
        """Return a Google Billing Account from Firestore."""
        return self.client.collection("google_billing_accounts").document(billing_account_name).get()

    def get_google_billing_accounts(self):
        """Return a list of Google Billing Accounts from Firestore."""
        return list(self.client.collection("google_billing_accounts").stream())

    # google budget notifications
    def get_google_budget_notifications(self):
        """Return a list of Google Budget Notifiations from Firestore."""
        return list(self.client.collection("google_budget_notifications").stream())

    # google invoices
    def get_google_invoices(self):
        """Return a list of Google Invoices from Firestore."""
        return list(self.client.collection("google_invoices").stream())

    # iam_policy_bindings (under google_billing_accounts)
    def get_iam_policy_bindings(self, billing_account_name):
        """Return a list of Google Billing Account IAM Policy Bindings from Firestore."""
        ref = self.client.collection("google_billing_accounts").document(billing_account_name)
        return list(ref.collection("iam_policy_bindings").stream())

    # projects (under google_billing_accounts)
    def get_projects(self, billing_account_name):
        """Return a list of Google Billing Account Projects from Firestore."""
        ref = self.client.collection("google_billing_accounts").document(billing_account_name)
        return list(ref.collection("projects").stream())

    # triggers
    def get_triggers(self):
        """Return a list of Triggers from Firestore."""
        return list(self.client.collection("triggers").stream())

    # webhooks
    def get_webhooks(self):
        """Return a list of Webhooks from Firestore."""
        return list(self.client.collection("webhooks").stream())
