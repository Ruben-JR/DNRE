# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import date
from dateutil.relativedelta import relativedelta

from odoo import Command
from odoo.tests.common import users, tagged, TransactionCase, warmup
from odoo.tools.misc import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT


@tagged("post_install", "-at_install")
class TestDiscussFullPerformance(TransactionCase):
    def setUp(self):
        super().setUp()
        self.users = self.env["res.users"].create(
            [
                {
                    "email": "e.e@example.com",
                    "groups_id": [Command.link(self.env.ref("base.group_user").id)],
                    "login": "emp",
                    "name": "Ernest Employee",
                    "notification_type": "inbox",
                    "signature": "--\nErnest",
                },
                {"name": "test1", "login": "test1", "email": "test1@example.com"},
                {"name": "test2", "login": "test2", "email": "test2@example.com"},
                {"name": "test3", "login": "test3"},
                {"name": "test4", "login": "test4"},
                {"name": "test5", "login": "test5"},
                {"name": "test6", "login": "test6"},
                {"name": "test7", "login": "test7"},
                {"name": "test8", "login": "test8"},
                {"name": "test9", "login": "test9"},
                {"name": "test10", "login": "test10"},
                {"name": "test11", "login": "test11"},
                {"name": "test12", "login": "test12"},
                {"name": "test13", "login": "test13"},
                {"name": "test14", "login": "test14"},
                {"name": "test15", "login": "test15"},
            ]
        )
        self.employees = self.env["hr.employee"].create(
            [
                {
                    "user_id": user.id,
                }
                for user in self.users
            ]
        )
        self.leave_type = self.env["hr.leave.type"].create(
            {
                "requires_allocation": "no",
                "name": "Legal Leaves",
                "time_type": "leave",
            }
        )
        self.leaves = self.env["hr.leave"].create(
            [
                {
                    "date_from": date.today() + relativedelta(days=-2),
                    "date_to": date.today() + relativedelta(days=2),
                    "employee_id": employee.id,
                    "holiday_status_id": self.leave_type.id,
                }
                for employee in self.employees
            ]
        )

    @users("emp")
    @warmup
    def test_init_messaging(self):
        """Test performance of `_init_messaging`."""
        channel_general = self.env.ref(
            "mail.channel_all_employees"
        )  # Unfortunately #general cannot be deleted. Assertions below assume data from a fresh db with demo.
        self.env["mail.channel"].sudo().search(
            [("id", "!=", channel_general.id)]
        ).unlink()
        user_root = self.env.ref("base.user_root")
        # create public channels
        channel_channel_public_1 = self.env["mail.channel"].browse(
            self.env["mail.channel"].channel_create(name="public 1", privacy="public")[
                "id"
            ]
        )
        channel_channel_public_1.add_members(
            (
                self.users[0]
                + self.users[2]
                + self.users[3]
                + self.users[4]
                + self.users[8]
            ).partner_id.ids
        )
        channel_channel_public_2 = self.env["mail.channel"].browse(
            self.env["mail.channel"].channel_create(name="public 2", privacy="public")[
                "id"
            ]
        )
        channel_channel_public_2.add_members(
            (
                self.users[0]
                + self.users[2]
                + self.users[4]
                + self.users[7]
                + self.users[9]
            ).partner_id.ids
        )
        # create groups channels
        channel_channel_group_1 = self.env["mail.channel"].browse(
            self.env["mail.channel"].channel_create(name="group 1", privacy="groups")[
                "id"
            ]
        )
        channel_channel_group_1.add_members(
            (
                self.users[0]
                + self.users[2]
                + self.users[3]
                + self.users[6]
                + self.users[12]
            ).partner_id.ids
        )
        channel_channel_group_2 = self.env["mail.channel"].browse(
            self.env["mail.channel"].channel_create(name="group 2", privacy="groups")[
                "id"
            ]
        )
        channel_channel_group_2.add_members(
            (
                self.users[0]
                + self.users[2]
                + self.users[6]
                + self.users[7]
                + self.users[13]
            ).partner_id.ids
        )
        # create private channels
        channel_channel_private_1 = self.env["mail.channel"].browse(
            self.env["mail.channel"].channel_create(
                name="private 1", privacy="private"
            )["id"]
        )
        channel_channel_private_1.add_members(
            (
                self.users[0]
                + self.users[2]
                + self.users[3]
                + self.users[5]
                + self.users[10]
            ).partner_id.ids
        )
        channel_channel_private_2 = self.env["mail.channel"].browse(
            self.env["mail.channel"].channel_create(
                name="private 2", privacy="private"
            )["id"]
        )
        channel_channel_private_2.add_members(
            (
                self.users[0]
                + self.users[2]
                + self.users[5]
                + self.users[7]
                + self.users[11]
            ).partner_id.ids
        )
        # create chats
        channel_chat_1 = self.env["mail.channel"].browse(
            self.env["mail.channel"].channel_get(
                (self.users[0] + self.users[14]).partner_id.ids
            )["id"]
        )
        channel_chat_2 = self.env["mail.channel"].browse(
            self.env["mail.channel"].channel_get(
                (self.users[0] + self.users[15]).partner_id.ids
            )["id"]
        )
        channel_chat_3 = self.env["mail.channel"].browse(
            self.env["mail.channel"].channel_get(
                (self.users[0] + self.users[2]).partner_id.ids
            )["id"]
        )
        channel_chat_4 = self.env["mail.channel"].browse(
            self.env["mail.channel"].channel_get(
                (self.users[0] + self.users[3]).partner_id.ids
            )["id"]
        )
        # create groups
        channel_group_1 = self.env["mail.channel"].browse(
            self.env["mail.channel"].create_group(
                (self.users[0] + self.users[12]).partner_id.ids
            )["id"]
        )
        # create livechats
        im_livechat_channel = (
            self.env["im_livechat.channel"]
            .sudo()
            .create({"name": "support", "user_ids": [Command.link(self.users[0].id)]})
        )
        self.users[0].im_status = "online"  # make available for livechat (ignore leave)
        channel_livechat_1 = self.env["mail.channel"].browse(
            im_livechat_channel._open_livechat_mail_channel(
                anonymous_name="anon 1",
                previous_operator_id=self.users[0].partner_id.id,
                user_id=self.users[1].id,
                country_id=self.env.ref("base.in").id,
            )["id"]
        )
        channel_livechat_1.with_user(self.users[1]).message_post(body="test")
        channel_livechat_2 = self.env["mail.channel"].browse(
            im_livechat_channel.with_user(
                self.env.ref("base.public_user")
            )._open_livechat_mail_channel(
                anonymous_name="anon 2",
                previous_operator_id=self.users[0].partner_id.id,
                country_id=self.env.ref("base.be").id,
            )[
                "id"
            ]
        )
        channel_livechat_2.with_user(
            self.env.ref("base.public_user")
        ).sudo().message_post(body="test")
        # add needaction
        self.users[0].notification_type = "inbox"
        message = channel_channel_public_1.message_post(
            body="test",
            message_type="comment",
            author_id=self.users[2].partner_id.id,
            partner_ids=self.users[0].partner_id.ids,
        )
        # add star
        message.toggle_message_starred()
        self.env.company.sudo().name = "YourCompany"

        self.maxDiff = None
        self.users[0].flush()
        self.users[0].invalidate_cache()
        with self.assertQueryCount(emp=90):  # ent: 89
            init_messaging = self.users[0].with_user(self.users[0])._init_messaging()

        self.assertEqual(
            init_messaging,
            {
                "needaction_inbox_counter": 1,
                "starred_counter": 1,
                "channels": [
                    {
                        "avatarCacheKey": channel_general._get_avatar_cache_key(),
                        "channel_type": "channel",
                        "create_uid": user_root.id,
                        "custom_channel_name": False,
                        "defaultDisplayMode": False,
                        "description": "General announcements for all employees.",
                        "group_based_subscription": True,
                        "id": channel_general.id,
                        "invitedGuests": [("insert", [])],
                        "invitedPartners": [("insert", [])],
                        "is_minimized": False,
                        "is_pinned": True,
                        "last_interest_dt": channel_general.channel_last_seen_partner_ids.filtered(
                            lambda p: p.partner_id == self.users[0].partner_id
                        ).last_interest_dt.strftime(
                            DEFAULT_SERVER_DATETIME_FORMAT
                        ),
                        "last_message_id": next(
                            res["message_id"]
                            for res in channel_general._channel_last_message_ids()
                        ),
                        "memberCount": len(
                            self.env.ref("base.group_user").users | user_root
                        ),
                        "message_needaction_counter": 0,
                        "message_unread_counter": 5,
                        "name": "general",
                        "public": "groups",
                        "rtcSessions": [("insert", [])],
                        "seen_message_id": False,
                        "state": "open",
                        "uuid": channel_general.uuid,
                    },
                    {
                        "avatarCacheKey": channel_channel_public_1._get_avatar_cache_key(),
                        "channel_type": "channel",
                        "create_uid": self.env.user.id,
                        "custom_channel_name": False,
                        "defaultDisplayMode": False,
                        "description": False,
                        "group_based_subscription": False,
                        "id": channel_channel_public_1.id,
                        "invitedGuests": [("insert", [])],
                        "invitedPartners": [("insert", [])],
                        "is_minimized": False,
                        "is_pinned": True,
                        "last_interest_dt": channel_channel_public_1.channel_last_seen_partner_ids.filtered(
                            lambda p: p.partner_id == self.users[0].partner_id
                        ).last_interest_dt.strftime(
                            DEFAULT_SERVER_DATETIME_FORMAT
                        ),
                        "last_message_id": next(
                            res["message_id"]
                            for res in channel_channel_public_1._channel_last_message_ids()
                        ),
                        "message_needaction_counter": 1,
                        "memberCount": 5,
                        "message_unread_counter": 0,
                        "name": "public 1",
                        "public": "public",
                        "rtcSessions": [("insert", [])],
                        "seen_message_id": next(
                            res["message_id"]
                            for res in channel_channel_public_1._channel_last_message_ids()
                        ),
                        "state": "open",
                        "uuid": channel_channel_public_1.uuid,
                    },
                    {
                        "avatarCacheKey": channel_channel_public_2._get_avatar_cache_key(),
                        "channel_type": "channel",
                        "create_uid": self.env.user.id,
                        "custom_channel_name": False,
                        "defaultDisplayMode": False,
                        "description": False,
                        "group_based_subscription": False,
                        "id": channel_channel_public_2.id,
                        "invitedGuests": [("insert", [])],
                        "invitedPartners": [("insert", [])],
                        "is_minimized": False,
                        "is_pinned": True,
                        "last_interest_dt": channel_channel_public_2.channel_last_seen_partner_ids.filtered(
                            lambda p: p.partner_id == self.users[0].partner_id
                        ).last_interest_dt.strftime(
                            DEFAULT_SERVER_DATETIME_FORMAT
                        ),
                        "last_message_id": next(
                            res["message_id"]
                            for res in channel_channel_public_2._channel_last_message_ids()
                        ),
                        "memberCount": 5,
                        "message_needaction_counter": 0,
                        "message_unread_counter": 0,
                        "name": "public 2",
                        "public": "public",
                        "rtcSessions": [("insert", [])],
                        "seen_message_id": next(
                            res["message_id"]
                            for res in channel_channel_public_2._channel_last_message_ids()
                        ),
                        "state": "open",
                        "uuid": channel_channel_public_2.uuid,
                    },
                    {
                        "avatarCacheKey": channel_channel_group_1._get_avatar_cache_key(),
                        "channel_type": "channel",
                        "create_uid": self.env.user.id,
                        "custom_channel_name": False,
                        "defaultDisplayMode": False,
                        "description": False,
                        "group_based_subscription": False,
                        "id": channel_channel_group_1.id,
                        "invitedGuests": [("insert", [])],
                        "invitedPartners": [("insert", [])],
                        "is_minimized": False,
                        "is_pinned": True,
                        "last_interest_dt": channel_channel_group_1.channel_last_seen_partner_ids.filtered(
                            lambda p: p.partner_id == self.users[0].partner_id
                        ).last_interest_dt.strftime(
                            DEFAULT_SERVER_DATETIME_FORMAT
                        ),
                        "last_message_id": next(
                            res["message_id"]
                            for res in channel_channel_group_1._channel_last_message_ids()
                        ),
                        "memberCount": 5,
                        "message_needaction_counter": 0,
                        "message_unread_counter": 0,
                        "name": "group 1",
                        "public": "groups",
                        "rtcSessions": [("insert", [])],
                        "seen_message_id": next(
                            res["message_id"]
                            for res in channel_channel_group_1._channel_last_message_ids()
                        ),
                        "state": "open",
                        "uuid": channel_channel_group_1.uuid,
                    },
                    {
                        "avatarCacheKey": channel_channel_group_2._get_avatar_cache_key(),
                        "channel_type": "channel",
                        "create_uid": self.env.user.id,
                        "custom_channel_name": False,
                        "defaultDisplayMode": False,
                        "description": False,
                        "group_based_subscription": False,
                        "id": channel_channel_group_2.id,
                        "invitedGuests": [("insert", [])],
                        "invitedPartners": [("insert", [])],
                        "is_minimized": False,
                        "is_pinned": True,
                        "last_interest_dt": channel_channel_group_2.channel_last_seen_partner_ids.filtered(
                            lambda p: p.partner_id == self.users[0].partner_id
                        ).last_interest_dt.strftime(
                            DEFAULT_SERVER_DATETIME_FORMAT
                        ),
                        "last_message_id": next(
                            res["message_id"]
                            for res in channel_channel_group_2._channel_last_message_ids()
                        ),
                        "memberCount": 5,
                        "message_needaction_counter": 0,
                        "message_unread_counter": 0,
                        "name": "group 2",
                        "public": "groups",
                        "rtcSessions": [("insert", [])],
                        "seen_message_id": next(
                            res["message_id"]
                            for res in channel_channel_group_2._channel_last_message_ids()
                        ),
                        "state": "open",
                        "uuid": channel_channel_group_2.uuid,
                    },
                    {
                        "avatarCacheKey": channel_channel_private_1._get_avatar_cache_key(),
                        "channel_type": "channel",
                        "create_uid": self.env.user.id,
                        "custom_channel_name": False,
                        "defaultDisplayMode": False,
                        "description": False,
                        "group_based_subscription": False,
                        "id": channel_channel_private_1.id,
                        "invitedGuests": [("insert", [])],
                        "invitedPartners": [("insert", [])],
                        "is_minimized": False,
                        "is_pinned": True,
                        "last_interest_dt": channel_channel_private_1.channel_last_seen_partner_ids.filtered(
                            lambda p: p.partner_id == self.users[0].partner_id
                        ).last_interest_dt.strftime(
                            DEFAULT_SERVER_DATETIME_FORMAT
                        ),
                        "last_message_id": next(
                            res["message_id"]
                            for res in channel_channel_private_1._channel_last_message_ids()
                        ),
                        "memberCount": 5,
                        "message_needaction_counter": 0,
                        "message_unread_counter": 0,
                        "name": "private 1",
                        "public": "private",
                        "rtcSessions": [("insert", [])],
                        "seen_message_id": next(
                            res["message_id"]
                            for res in channel_channel_private_1._channel_last_message_ids()
                        ),
                        "state": "open",
                        "uuid": channel_channel_private_1.uuid,
                    },
                    {
                        "avatarCacheKey": channel_channel_private_2._get_avatar_cache_key(),
                        "channel_type": "channel",
                        "create_uid": self.env.user.id,
                        "custom_channel_name": False,
                        "defaultDisplayMode": False,
                        "description": False,
                        "group_based_subscription": False,
                        "id": channel_channel_private_2.id,
                        "invitedGuests": [("insert", [])],
                        "invitedPartners": [("insert", [])],
                        "is_minimized": False,
                        "is_pinned": True,
                        "last_interest_dt": channel_channel_private_2.channel_last_seen_partner_ids.filtered(
                            lambda p: p.partner_id == self.users[0].partner_id
                        ).last_interest_dt.strftime(
                            DEFAULT_SERVER_DATETIME_FORMAT
                        ),
                        "last_message_id": next(
                            res["message_id"]
                            for res in channel_channel_private_2._channel_last_message_ids()
                        ),
                        "memberCount": 5,
                        "message_needaction_counter": 0,
                        "message_unread_counter": 0,
                        "name": "private 2",
                        "public": "private",
                        "rtcSessions": [("insert", [])],
                        "seen_message_id": next(
                            res["message_id"]
                            for res in channel_channel_private_2._channel_last_message_ids()
                        ),
                        "state": "open",
                        "uuid": channel_channel_private_2.uuid,
                    },
                    {
                        "avatarCacheKey": channel_group_1._get_avatar_cache_key(),
                        "channel_type": "group",
                        "create_uid": self.env.user.id,
                        "custom_channel_name": False,
                        "defaultDisplayMode": False,
                        "description": False,
                        "group_based_subscription": False,
                        "guestMembers": [("insert", [])],
                        "id": channel_group_1.id,
                        "invitedGuests": [("insert", [])],
                        "invitedPartners": [("insert", [])],
                        "is_minimized": False,
                        "is_pinned": True,
                        "last_interest_dt": channel_group_1.channel_last_seen_partner_ids.filtered(
                            lambda p: p.partner_id == self.users[0].partner_id
                        ).last_interest_dt.strftime(
                            DEFAULT_SERVER_DATETIME_FORMAT
                        ),
                        "last_message_id": False,
                        "memberCount": 2,
                        "members": [
                            {
                                "active": True,
                                "display_name": "Ernest Employee",
                                "email": "e.e@example.com",
                                "id": self.users[0].partner_id.id,
                                "im_status": "offline",
                                "is_internal_user": True,
                                "name": "Ernest Employee",
                                "out_of_office_date_end": self.leaves.filtered(
                                    lambda l: l.employee_id.user_id == self.users[0]
                                ).date_to.strftime(DEFAULT_SERVER_DATE_FORMAT),
                                "user_id": self.users[0].id,
                            },
                            {
                                "active": True,
                                "display_name": "test12",
                                "email": False,
                                "id": self.users[12].partner_id.id,
                                "im_status": "offline",
                                "is_internal_user": True,
                                "name": "test12",
                                "out_of_office_date_end": self.leaves.filtered(
                                    lambda l: l.employee_id.user_id == self.users[12]
                                ).date_to.strftime(DEFAULT_SERVER_DATE_FORMAT),
                                "user_id": self.users[12].id,
                            },
                        ],
                        "message_needaction_counter": 0,
                        "message_unread_counter": 0,
                        "name": "",
                        "public": "private",
                        "rtcSessions": [("insert", [])],
                        "seen_message_id": False,
                        "seen_partners_info": [
                            {
                                "fetched_message_id": False,
                                "id": channel_group_1.channel_last_seen_partner_ids.filtered(
                                    lambda p: p.partner_id == self.users[0].partner_id
                                ).id,
                                "partner_id": self.users[0].partner_id.id,
                                "seen_message_id": False,
                            },
                            {
                                "fetched_message_id": False,
                                "id": channel_group_1.channel_last_seen_partner_ids.filtered(
                                    lambda p: p.partner_id == self.users[12].partner_id
                                ).id,
                                "partner_id": self.users[12].partner_id.id,
                                "seen_message_id": False,
                            },
                        ],
                        "state": "open",
                        "uuid": channel_group_1.uuid,
                    },
                    {
                        "avatarCacheKey": channel_chat_1._get_avatar_cache_key(),
                        "channel_type": "chat",
                        "create_uid": self.env.user.id,
                        "custom_channel_name": False,
                        "defaultDisplayMode": False,
                        "description": False,
                        "group_based_subscription": False,
                        "guestMembers": [("insert", [])],
                        "id": channel_chat_1.id,
                        "invitedGuests": [("insert", [])],
                        "invitedPartners": [("insert", [])],
                        "is_minimized": False,
                        "is_pinned": True,
                        "last_interest_dt": channel_chat_1.channel_last_seen_partner_ids.filtered(
                            lambda p: p.partner_id == self.users[0].partner_id
                        ).last_interest_dt.strftime(
                            DEFAULT_SERVER_DATETIME_FORMAT
                        ),
                        "last_message_id": False,
                        "memberCount": 2,
                        "members": [
                            {
                                "active": True,
                                "display_name": "Ernest Employee",
                                "email": "e.e@example.com",
                                "id": self.users[0].partner_id.id,
                                "im_status": "offline",
                                "is_internal_user": True,
                                "name": "Ernest Employee",
                                "out_of_office_date_end": self.leaves.filtered(
                                    lambda l: l.employee_id.user_id == self.users[0]
                                ).date_to.strftime(DEFAULT_SERVER_DATE_FORMAT),
                                "user_id": self.users[0].id,
                            },
                            {
                                "active": True,
                                "display_name": "test14",
                                "email": False,
                                "id": self.users[14].partner_id.id,
                                "im_status": "offline",
                                "is_internal_user": True,
                                "name": "test14",
                                "out_of_office_date_end": self.leaves.filtered(
                                    lambda l: l.employee_id.user_id == self.users[14]
                                ).date_to.strftime(DEFAULT_SERVER_DATE_FORMAT),
                                "user_id": self.users[14].id,
                            },
                        ],
                        "message_needaction_counter": 0,
                        "message_unread_counter": 0,
                        "name": "Ernest Employee, test14",
                        "public": "private",
                        "rtcSessions": [("insert", [])],
                        "seen_partners_info": [
                            {
                                "fetched_message_id": False,
                                "id": channel_chat_1.channel_last_seen_partner_ids.filtered(
                                    lambda p: p.partner_id == self.users[0].partner_id
                                ).id,
                                "partner_id": self.users[0].partner_id.id,
                                "seen_message_id": False,
                            },
                            {
                                "fetched_message_id": False,
                                "id": channel_chat_1.channel_last_seen_partner_ids.filtered(
                                    lambda p: p.partner_id == self.users[14].partner_id
                                ).id,
                                "partner_id": self.users[14].partner_id.id,
                                "seen_message_id": False,
                            },
                        ],
                        "seen_message_id": False,
                        "state": "open",
                        "uuid": channel_chat_1.uuid,
                    },
                    {
                        "avatarCacheKey": channel_chat_2._get_avatar_cache_key(),
                        "channel_type": "chat",
                        "create_uid": self.env.user.id,
                        "custom_channel_name": False,
                        "defaultDisplayMode": False,
                        "description": False,
                        "group_based_subscription": False,
                        "guestMembers": [("insert", [])],
                        "id": channel_chat_2.id,
                        "invitedGuests": [("insert", [])],
                        "invitedPartners": [("insert", [])],
                        "is_minimized": False,
                        "is_pinned": True,
                        "last_interest_dt": channel_chat_2.channel_last_seen_partner_ids.filtered(
                            lambda p: p.partner_id == self.users[0].partner_id
                        ).last_interest_dt.strftime(
                            DEFAULT_SERVER_DATETIME_FORMAT
                        ),
                        "last_message_id": False,
                        "memberCount": 2,
                        "members": [
                            {
                                "active": True,
                                "display_name": "Ernest Employee",
                                "email": "e.e@example.com",
                                "id": self.users[0].partner_id.id,
                                "im_status": "offline",
                                "is_internal_user": True,
                                "name": "Ernest Employee",
                                "out_of_office_date_end": self.leaves.filtered(
                                    lambda l: l.employee_id.user_id == self.users[0]
                                ).date_to.strftime(DEFAULT_SERVER_DATE_FORMAT),
                                "user_id": self.users[0].id,
                            },
                            {
                                "active": True,
                                "display_name": "test15",
                                "email": False,
                                "id": self.users[15].partner_id.id,
                                "im_status": "offline",
                                "is_internal_user": True,
                                "name": "test15",
                                "out_of_office_date_end": self.leaves.filtered(
                                    lambda l: l.employee_id.user_id == self.users[15]
                                ).date_to.strftime(DEFAULT_SERVER_DATE_FORMAT),
                                "user_id": self.users[15].id,
                            },
                        ],
                        "message_needaction_counter": 0,
                        "message_unread_counter": 0,
                        "name": "Ernest Employee, test15",
                        "public": "private",
                        "rtcSessions": [("insert", [])],
                        "seen_partners_info": [
                            {
                                "fetched_message_id": False,
                                "id": channel_chat_2.channel_last_seen_partner_ids.filtered(
                                    lambda p: p.partner_id == self.users[0].partner_id
                                ).id,
                                "partner_id": self.users[0].partner_id.id,
                                "seen_message_id": False,
                            },
                            {
                                "fetched_message_id": False,
                                "id": channel_chat_2.channel_last_seen_partner_ids.filtered(
                                    lambda p: p.partner_id == self.users[15].partner_id
                                ).id,
                                "partner_id": self.users[15].partner_id.id,
                                "seen_message_id": False,
                            },
                        ],
                        "seen_message_id": False,
                        "state": "open",
                        "uuid": channel_chat_2.uuid,
                    },
                    {
                        "avatarCacheKey": channel_chat_3._get_avatar_cache_key(),
                        "channel_type": "chat",
                        "create_uid": self.env.user.id,
                        "custom_channel_name": False,
                        "defaultDisplayMode": False,
                        "description": False,
                        "group_based_subscription": False,
                        "guestMembers": [("insert", [])],
                        "id": channel_chat_3.id,
                        "invitedGuests": [("insert", [])],
                        "invitedPartners": [("insert", [])],
                        "is_minimized": False,
                        "is_pinned": True,
                        "last_interest_dt": channel_chat_3.channel_last_seen_partner_ids.filtered(
                            lambda p: p.partner_id == self.users[0].partner_id
                        ).last_interest_dt.strftime(
                            DEFAULT_SERVER_DATETIME_FORMAT
                        ),
                        "last_message_id": False,
                        "memberCount": 2,
                        "members": [
                            {
                                "active": True,
                                "display_name": "Ernest Employee",
                                "email": "e.e@example.com",
                                "id": self.users[0].partner_id.id,
                                "im_status": "offline",
                                "is_internal_user": True,
                                "name": "Ernest Employee",
                                "out_of_office_date_end": self.leaves.filtered(
                                    lambda l: l.employee_id.user_id == self.users[0]
                                ).date_to.strftime(DEFAULT_SERVER_DATE_FORMAT),
                                "user_id": self.users[0].id,
                            },
                            {
                                "active": True,
                                "display_name": "test2",
                                "email": "test2@example.com",
                                "id": self.users[2].partner_id.id,
                                "im_status": "offline",
                                "is_internal_user": True,
                                "name": "test2",
                                "out_of_office_date_end": self.leaves.filtered(
                                    lambda l: l.employee_id.user_id == self.users[2]
                                ).date_to.strftime(DEFAULT_SERVER_DATE_FORMAT),
                                "user_id": self.users[2].id,
                            },
                        ],
                        "message_needaction_counter": 0,
                        "message_unread_counter": 0,
                        "name": "Ernest Employee, test2",
                        "public": "private",
                        "rtcSessions": [("insert", [])],
                        "seen_partners_info": [
                            {
                                "fetched_message_id": False,
                                "id": channel_chat_3.channel_last_seen_partner_ids.filtered(
                                    lambda p: p.partner_id == self.users[0].partner_id
                                ).id,
                                "partner_id": self.users[0].partner_id.id,
                                "seen_message_id": False,
                            },
                            {
                                "fetched_message_id": False,
                                "id": channel_chat_3.channel_last_seen_partner_ids.filtered(
                                    lambda p: p.partner_id == self.users[2].partner_id
                                ).id,
                                "partner_id": self.users[2].partner_id.id,
                                "seen_message_id": False,
                            },
                        ],
                        "seen_message_id": False,
                        "state": "open",
                        "uuid": channel_chat_3.uuid,
                    },
                    {
                        "avatarCacheKey": channel_chat_4._get_avatar_cache_key(),
                        "channel_type": "chat",
                        "create_uid": self.env.user.id,
                        "custom_channel_name": False,
                        "defaultDisplayMode": False,
                        "description": False,
                        "group_based_subscription": False,
                        "guestMembers": [("insert", [])],
                        "id": channel_chat_4.id,
                        "invitedGuests": [("insert", [])],
                        "invitedPartners": [("insert", [])],
                        "is_minimized": False,
                        "is_pinned": True,
                        "last_interest_dt": channel_chat_4.channel_last_seen_partner_ids.filtered(
                            lambda p: p.partner_id == self.users[0].partner_id
                        ).last_interest_dt.strftime(
                            DEFAULT_SERVER_DATETIME_FORMAT
                        ),
                        "last_message_id": False,
                        "memberCount": 2,
                        "members": [
                            {
                                "active": True,
                                "display_name": "Ernest Employee",
                                "email": "e.e@example.com",
                                "id": self.users[0].partner_id.id,
                                "im_status": "offline",
                                "is_internal_user": True,
                                "name": "Ernest Employee",
                                "out_of_office_date_end": self.leaves.filtered(
                                    lambda l: l.employee_id.user_id == self.users[0]
                                ).date_to.strftime(DEFAULT_SERVER_DATE_FORMAT),
                                "user_id": self.users[0].id,
                            },
                            {
                                "active": True,
                                "display_name": "test3",
                                "email": False,
                                "id": self.users[3].partner_id.id,
                                "im_status": "offline",
                                "is_internal_user": True,
                                "name": "test3",
                                "out_of_office_date_end": self.leaves.filtered(
                                    lambda l: l.employee_id.user_id == self.users[3]
                                ).date_to.strftime(DEFAULT_SERVER_DATE_FORMAT),
                                "user_id": self.users[3].id,
                            },
                        ],
                        "message_needaction_counter": 0,
                        "message_unread_counter": 0,
                        "name": "Ernest Employee, test3",
                        "public": "private",
                        "rtcSessions": [("insert", [])],
                        "seen_partners_info": [
                            {
                                "fetched_message_id": False,
                                "id": channel_chat_4.channel_last_seen_partner_ids.filtered(
                                    lambda p: p.partner_id == self.users[0].partner_id
                                ).id,
                                "partner_id": self.users[0].partner_id.id,
                                "seen_message_id": False,
                            },
                            {
                                "fetched_message_id": False,
                                "id": channel_chat_4.channel_last_seen_partner_ids.filtered(
                                    lambda p: p.partner_id == self.users[3].partner_id
                                ).id,
                                "partner_id": self.users[3].partner_id.id,
                                "seen_message_id": False,
                            },
                        ],
                        "seen_message_id": False,
                        "state": "open",
                        "uuid": channel_chat_4.uuid,
                    },
                    {
                        "avatarCacheKey": channel_livechat_1._get_avatar_cache_key(),
                        "channel_type": "livechat",
                        "create_uid": self.env.user.id,
                        "custom_channel_name": False,
                        "defaultDisplayMode": False,
                        "description": False,
                        "group_based_subscription": False,
                        "guestMembers": [("insert", [])],
                        "id": channel_livechat_1.id,
                        "invitedGuests": [("insert", [])],
                        "invitedPartners": [("insert", [])],
                        "is_minimized": False,
                        "is_pinned": True,
                        "last_interest_dt": channel_livechat_1.channel_last_seen_partner_ids.filtered(
                            lambda p: p.partner_id == self.users[0].partner_id
                        ).last_interest_dt.strftime(
                            DEFAULT_SERVER_DATETIME_FORMAT
                        ),
                        "last_message_id": next(
                            res["message_id"]
                            for res in channel_livechat_1._channel_last_message_ids()
                        ),
                        "memberCount": 2,
                        "livechat_visitor": {
                            "country": False,
                            "id": self.users[1].partner_id.id,
                            "name": "test1",
                        },
                        "members": [
                            {
                                "active": True,
                                "email": False,
                                "id": self.users[0].partner_id.id,
                                "im_status": False,
                                "livechat_username": False,
                                "name": "Ernest Employee",
                            },
                            {
                                "active": True,
                                "email": False,
                                "id": self.users[1].partner_id.id,
                                "im_status": False,
                                "livechat_username": False,
                                "name": "test1",
                            },
                        ],
                        "message_needaction_counter": 0,
                        "message_unread_counter": 0,
                        "name": "test1 Ernest Employee",
                        "operator_pid": (
                            self.users[0].partner_id.id,
                            "Ernest Employee",
                        ),
                        "public": "private",
                        "rtcSessions": [("insert", [])],
                        "seen_partners_info": [
                            {
                                "fetched_message_id": False,
                                "id": channel_livechat_1.channel_last_seen_partner_ids.filtered(
                                    lambda p: p.partner_id == self.users[0].partner_id
                                ).id,
                                "partner_id": self.users[0].partner_id.id,
                                "seen_message_id": False,
                            },
                            {
                                "fetched_message_id": next(
                                    res["message_id"]
                                    for res in channel_livechat_1._channel_last_message_ids()
                                ),
                                "id": channel_livechat_1.channel_last_seen_partner_ids.filtered(
                                    lambda p: p.partner_id == self.users[1].partner_id
                                ).id,
                                "partner_id": self.users[1].partner_id.id,
                                "seen_message_id": next(
                                    res["message_id"]
                                    for res in channel_livechat_1._channel_last_message_ids()
                                ),
                            },
                        ],
                        "seen_message_id": False,
                        "state": "open",
                        "uuid": channel_livechat_1.uuid,
                    },
                    {
                        "avatarCacheKey": channel_livechat_2._get_avatar_cache_key(),
                        "channel_type": "livechat",
                        "create_uid": self.env.ref("base.public_user").id,
                        "custom_channel_name": False,
                        "defaultDisplayMode": False,
                        "description": False,
                        "group_based_subscription": False,
                        "guestMembers": [("insert", [])],
                        "id": channel_livechat_2.id,
                        "invitedGuests": [("insert", [])],
                        "invitedPartners": [("insert", [])],
                        "is_minimized": False,
                        "is_pinned": True,
                        "last_interest_dt": channel_livechat_2.channel_last_seen_partner_ids.filtered(
                            lambda p: p.partner_id == self.users[0].partner_id
                        ).last_interest_dt.strftime(
                            DEFAULT_SERVER_DATETIME_FORMAT
                        ),
                        "last_message_id": next(
                            res["message_id"]
                            for res in channel_livechat_2._channel_last_message_ids()
                        ),
                        "memberCount": 2,
                        "livechat_visitor": {
                            "country": (self.env.ref("base.be").id, "Belgium"),
                            "id": False,
                            "name": "anon 2",
                        },
                        "members": [
                            {
                                "active": False,
                                "email": False,
                                "id": self.env.ref("base.public_partner").id,
                                "im_status": False,
                                "livechat_username": False,
                                "name": "Public user",
                            },
                            {
                                "active": True,
                                "email": False,
                                "id": self.users[0].partner_id.id,
                                "im_status": False,
                                "livechat_username": False,
                                "name": "Ernest Employee",
                            },
                        ],
                        "message_needaction_counter": 0,
                        "message_unread_counter": 0,
                        "name": "anon 2 Ernest Employee",
                        "operator_pid": (
                            self.users[0].partner_id.id,
                            "Ernest Employee",
                        ),
                        "public": "private",
                        "rtcSessions": [("insert", [])],
                        "seen_partners_info": [
                            {
                                "fetched_message_id": next(
                                    res["message_id"]
                                    for res in channel_livechat_2._channel_last_message_ids()
                                ),
                                "id": channel_livechat_2.channel_last_seen_partner_ids.filtered(
                                    lambda p: p.partner_id
                                    == self.env.ref("base.public_partner")
                                ).id,
                                "partner_id": self.env.ref(
                                    "base.public_user"
                                ).partner_id.id,
                                "seen_message_id": next(
                                    res["message_id"]
                                    for res in channel_livechat_2._channel_last_message_ids()
                                ),
                            },
                            {
                                "fetched_message_id": False,
                                "id": channel_livechat_2.channel_last_seen_partner_ids.filtered(
                                    lambda p: p.partner_id == self.users[0].partner_id
                                ).id,
                                "partner_id": self.users[0].partner_id.id,
                                "seen_message_id": False,
                            },
                        ],
                        "seen_message_id": False,
                        "state": "open",
                        "uuid": channel_livechat_2.uuid,
                    },
                ],
                "companyName": "YourCompany",
                "mail_failures": [],
                "shortcodes": [
                    {
                        "description": False,
                        "id": 1,
                        "source": "hello",
                        "substitution": "Hello. How may I help you?",
                    },
                    {
                        "description": False,
                        "id": 2,
                        "source": "bye",
                        "substitution": "Thanks for your feedback. Good bye!",
                    },
                ],
                "menu_id": self.env["ir.model.data"]._xmlid_to_res_id(
                    "mail.menu_root_discuss"
                ),
                "partner_root": {
                    "active": False,
                    "display_name": "OdooBot",
                    "email": "odoobot@example.com",
                    "id": user_root.partner_id.id,
                    "im_status": "bot",
                    "is_internal_user": True,
                    "name": "OdooBot",
                    "out_of_office_date_end": False,
                    "user_id": False,
                },
                "public_partners": [
                    {
                        "active": False,
                        "display_name": "Public user",
                        "email": False,
                        "id": self.env.ref("base.public_partner").id,
                        "im_status": "im_partner",
                        "is_internal_user": False,
                        "name": "Public user",
                        "out_of_office_date_end": False,
                        "user_id": self.env.ref("base.public_user").id,
                    }
                ],
                "currentGuest": False,
                "current_partner": {
                    "active": True,
                    "display_name": "Ernest Employee",
                    "email": "e.e@example.com",
                    "id": self.users[0].partner_id.id,
                    "im_status": "offline",
                    "is_internal_user": True,
                    "name": "Ernest Employee",
                    "out_of_office_date_end": self.leaves.filtered(
                        lambda l: l.employee_id.user_id == self.users[0]
                    ).date_to.strftime(DEFAULT_SERVER_DATE_FORMAT),
                    "user_id": self.users[0].id,
                },
                "current_user_id": self.users[0].id,
                "current_user_settings": {
                    "id": self.env["res.users.settings"]
                    ._find_or_create_for_user(self.users[0])
                    .id,
                    "is_discuss_sidebar_category_channel_open": True,
                    "is_discuss_sidebar_category_chat_open": True,
                    "is_discuss_sidebar_category_livechat_open": True,
                    "push_to_talk_key": False,
                    "use_push_to_talk": False,
                    "user_id": (self.users[0].id, "Ernest Employee"),
                    "voice_active_duration": 0,
                    "volume_settings": [],
                },
            },
        )
