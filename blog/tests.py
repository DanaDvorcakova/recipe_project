from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from blog.models import Post, Comment
from django.urls import reverse

class PostModelTest(TestCase):

    def setUp(self):
        # Create users for the test
        self.user1 = User.objects.create_user(username='testuser1', password='password123')
        self.user2 = User.objects.create_user(username='testuser2', password='password123')

        # Create a post instance for testing
        self.post = Post.objects.create(
            title='Test Post',
            description='This is a test post description.',
            start_date=timezone.now().date(),
            status='Draft',
            ingredients='Test ingredients',
            instructions='Test instructions',
            cooking_time=30,
            category='Main Course',
            author=self.user1
        )

    def test_post_creation(self):
        """Test that a post is correctly created."""
        post = self.post
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.description, 'This is a test post description.')
        self.assertEqual(post.status, 'Draft')
        self.assertEqual(post.author.username, 'testuser1')
        self.assertEqual(post.cooking_time, 30)
        self.assertEqual(post.category, 'Main Course')

    def test_post_absolute_url(self):
        """Test the get_absolute_url method of the Post model."""
        post = self.post
        self.assertEqual(post.get_absolute_url(), f"/post/{post.pk}/")

    def test_total_likes(self):
        """Test that the total_likes method correctly counts the number of likes."""
        self.post.likes.add(self.user1, self.user2)
        self.assertEqual(self.post.total_likes(), 2)

    def test_total_saves(self):
        """Test that the total_saves method correctly counts the number of saves."""
        self.post.saved_by.add(self.user1)
        self.assertEqual(self.post.total_saves(), 1)

    def test_post_status_choices(self):
        """Test the valid status choices in Post model."""
        self.assertEqual(self.post.status, 'Draft')
        self.post.status = 'Published'
        self.post.save()
        self.assertEqual(self.post.status, 'Published')

    def test_category_choices(self):
        """Test the valid category choices in Post model."""
        self.assertEqual(self.post.category, 'Main Course')
        self.post.category = 'Dessert'
        self.post.save()
        self.assertEqual(self.post.category, 'Dessert')

    def test_add_stakeholders(self):
        """Test adding stakeholders to a post."""
        self.post.stakeholders.add(self.user1, self.user2)
        self.assertIn(self.user1, self.post.stakeholders.all())
        self.assertIn(self.user2, self.post.stakeholders.all())

    def test_create_comment(self):
        """Test that a comment can be created and linked to a post."""
        comment = Comment.objects.create(
            post=self.post,
            user=self.user1,
            content='This is a test comment.'
        )
        self.assertEqual(comment.post, self.post)
        self.assertEqual(comment.user, self.user1)
        self.assertEqual(comment.content, 'This is a test comment.')
        self.assertEqual(comment.date_posted.date(), timezone.now().date())

    def test_comment_ordering(self):
        """Test that comments are ordered by date_posted."""
        comment1 = Comment.objects.create(
            post=self.post,
            user=self.user1,
            content='First comment'
        )
        comment2 = Comment.objects.create(
            post=self.post,
            user=self.user2,
            content='Second comment'
        )
        comments = self.post.comments.all()
        self.assertEqual(comments[0], comment2)
        self.assertEqual(comments[1], comment1)

class PostViewTests(TestCase):

    def setUp(self):
        # Create users for the test
        self.user1 = User.objects.create_user(username='testuser1', password='password123')
        self.user2 = User.objects.create_user(username='testuser2', password='password123')

        # Create a post instance for testing
        self.post = Post.objects.create(
            title='Test Post',
            description='This is a test post description.',
            start_date=timezone.now().date(),
            status='Draft',
            ingredients='Test ingredients',
            instructions='Test instructions',
            cooking_time=30,
            category='Main Course',
            author=self.user1
        )

    def test_post_detail_view(self):
        """Test the post detail view."""
        response = self.client.get(f"/post/{self.post.pk}/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.post.description)

    def test_like_post_view(self):
        """Test liking a post."""
        self.client.login(username='testuser1', password='password123')
        response = self.client.post(f"/post/{self.post.pk}/like/")
        self.assertEqual(response.status_code, 200)
        self.post.refresh_from_db()
        self.assertEqual(self.post.total_likes(), 1)

    def test_save_post_view(self):
       """Test saving a post."""
       self.client.login(username='testuser1', password='password123')

     # Use reverse to get the URL dynamically
       url = reverse('toggle-save')  # Correct URL for toggle save
       response = self.client.post(url, {'post_id': self.post.pk})  # Sending post_id in the post request
       self.assertEqual(response.status_code, 200)  # This should now pass
       self.post.refresh_from_db()
       self.assertEqual(self.post.total_saves(), 1) 