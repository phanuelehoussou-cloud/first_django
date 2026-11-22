import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Choice, Question


def create_question(question_text, days):
    """Create a question with a publication date offset from now."""
    pub_date = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=pub_date)


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        question = Question(
            question_text="Future question",
            pub_date=timezone.now() + datetime.timedelta(days=30),
        )
        self.assertIs(question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        question = Question(
            question_text="Old question",
            pub_date=timezone.now() - datetime.timedelta(days=1, seconds=1),
        )
        self.assertIs(question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        question = Question(
            question_text="Recent question",
            pub_date=timezone.now() - datetime.timedelta(hours=1),
        )
        self.assertIs(question.was_published_recently(), True)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question_is_displayed(self):
        question = create_question("Past question", days=-1)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [question])

    def test_future_question_is_hidden(self):
        create_question("Future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_questions_are_ordered_newest_first(self):
        older = create_question("Older", days=-30)
        newer = create_question("Newer", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [newer, older])

    def test_only_five_latest_questions_are_listed(self):
        questions = [create_question(f"Question {day}", days=day) for day in range(-7, 0)]
        response = self.client.get(reverse("polls:index"))
        expected = list(reversed(questions[-5:]))
        self.assertQuerySetEqual(response.context["latest_question_list"], expected)


class QuestionDetailViewTests(TestCase):
    def test_past_question_is_displayed(self):
        question = create_question("Past question", days=-1)
        response = self.client.get(reverse("polls:detail", args=(question.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, question.question_text)

    def test_future_question_returns_404(self):
        question = create_question("Future question", days=30)
        response = self.client.get(reverse("polls:detail", args=(question.id,)))
        self.assertEqual(response.status_code, 404)


class VoteViewTests(TestCase):
    def setUp(self):
        self.question = create_question("A poll", days=-1)
        self.choice = Choice.objects.create(
            question=self.question,
            choice_text="First answer",
            votes=0,
        )

    def test_vote_increments_choice_and_redirects(self):
        response = self.client.post(
            reverse("polls:vote", args=(self.question.id,)),
            {"choice": self.choice.id},
        )
        self.choice.refresh_from_db()
        self.assertEqual(self.choice.votes, 1)
        self.assertRedirects(response, reverse("polls:results", args=(self.question.id,)))

    def test_vote_without_choice_shows_error(self):
        response = self.client.post(reverse("polls:vote", args=(self.question.id,)), {})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["error_message"], "You didn't select a choice.")
        self.choice.refresh_from_db()
        self.assertEqual(self.choice.votes, 0)

    def test_get_request_cannot_submit_vote(self):
        response = self.client.get(reverse("polls:vote", args=(self.question.id,)))
        self.assertEqual(response.status_code, 405)
