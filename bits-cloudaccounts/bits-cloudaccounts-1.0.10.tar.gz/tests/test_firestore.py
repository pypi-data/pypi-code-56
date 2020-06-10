# -*- coding: utf-8 -*-
"""Tests for Firestore class."""

import unittest

from bits.cloudaccounts import firestore


class TestFirestore(unittest.TestCase):
    """Test Firestore class."""

    def setUp(self):
        """Set up the tests."""
        self.amazon_account_name = "374741154730"
        self.billing_account_name = "00A539-93294F-AC9B6F"
        self.budget_name = "XHCVHIQYECSFQJI2QSVXVGKEJ4000000"

    # @patch.dict(os.environ, {"GCP_PROJECT": "broad-cloudaccounts-app-dev"})
    def test_gcp_project(self):
        """Test __init__() with GCP_PROJECT."""
        fs = firestore.Firestore()
        self.assertTrue(fs)

    # @patch.dict(os.environ, {"GOOGLE_CLOUD_PROJECT": "broad-cloudaccounts-app-dev"})
    def test_google_cloud_project(self):
        """Test __init__() with GOOGLE_CLOUD_PROJECT."""
        fs = firestore.Firestore()
        self.assertTrue(fs)

    def test_get_accounts(self):
        """Test get_accounts()."""
        fs = firestore.Firestore()
        accounts = list(fs.get_accounts())
        print(f"Found {len(accounts)} accounts in Firestore.")

    def test_get_actions(self):
        """Test get_actions()."""
        fs = firestore.Firestore()
        actions = list(fs.get_actions())
        print(f"Found {len(actions)} actions in Firestore.")

    def test_get_amazon_account(self):
        """Test get_amazon_account()."""
        fs = firestore.Firestore()
        amazon_account = fs.get_amazon_account(self.amazon_account_name).to_dict()
        print(amazon_account)

    def test_get_amazon_accounts(self):
        """Test get_amazon_accounts()."""
        fs = firestore.Firestore()
        amazon_accounts = list(fs.get_amazon_accounts())
        print(f"Found {len(amazon_accounts)} Amazon accounts in Firestore.")

    def test_get_budget(self):
        """Test get_budget()."""
        fs = firestore.Firestore()
        budget = fs.get_budget(self.billing_account_name, self.budget_name).to_dict()
        print(budget)

    def test_get_budgets(self):
        """Test get_budgets()."""
        fs = firestore.Firestore()
        budgets = list(fs.get_budgets(self.billing_account_name))
        print(f"Found {len(budgets)} budgets for {self.billing_account_name} in Firestore.")

    def test_get_cost_objects(self):
        """Test get_cost_objects()."""
        fs = firestore.Firestore()
        cost_objects = list(fs.get_cost_objects())
        print(f"Found {len(cost_objects)} cost objects in Firestore.")

    def test_get_google_billing_account(self):
        """Test get_google_billing_account()."""
        fs = firestore.Firestore()
        account = fs.get_google_billing_account(self.billing_account_name).to_dict()
        print(account)

    def test_get_google_billing_accounts(self):
        """Test get_google_billing_accounts()."""
        fs = firestore.Firestore()
        google_billing_accounts = list(fs.get_google_billing_accounts())
        print(f"Found {len(google_billing_accounts)} Google billing accounts in Firestore.")

    def test_get_google_budget_notifications(self):
        """Test get_google_budget_notifications()."""
        fs = firestore.Firestore()
        google_budget_notifications = list(fs.get_google_budget_notifications())
        print(f"Found {len(google_budget_notifications)} Google budget notifications in Firestore.")

    def test_get_google_invoices(self):
        """Test get_google_invoices()."""
        fs = firestore.Firestore()
        invoices = list(fs.get_google_invoices())
        print(f"Found {len(invoices)} Google invoices in Firestore.")

    def test_get_iam_policy_bindings(self):
        """Test get_iam_policy_bindings()."""
        fs = firestore.Firestore()
        iam_policy_bindings = list(fs.get_iam_policy_bindings(self.billing_account_name))
        print(f"Found {len(iam_policy_bindings)} IAM policy bindings for {self.billing_account_name} in Firestore.")

    def test_get_projects(self):
        """Test get_projects()."""
        fs = firestore.Firestore()
        projects = list(fs.get_projects(self.billing_account_name))
        print(f"Found {len(projects)} projects for {self.billing_account_name} in Firestore.")

    def test_get_google_triggers(self):
        """Test get_google_triggers()."""
        fs = firestore.Firestore()
        triggers = list(fs.get_triggers())
        print(f"Found {len(triggers)} triggers in Firestore.")

    def test_get_google_webhooks(self):
        """Test get_google_webhooks()."""
        fs = firestore.Firestore()
        webhooks = list(fs.get_webhooks())
        print(f"Found {len(webhooks)} webhooks in Firestore.")
