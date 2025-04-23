from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Category, Reporter, Article, Tag


class CategoryModelTest(TestCase):
    """Test cases for the Category model"""
    
    def test_category_creation(self):
        """Test creating a category and checking slug generation"""
        category = Category.objects.create(name="Technology")
        self.assertEqual(category.name, "Technology")
        self.assertEqual(category.slug, "technology")
        self.assertEqual(str(category), "Technology")


class ReporterModelTest(TestCase):
    """Test cases for the Reporter model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser",
            first_name="Test",
            last_name="User",
            email="test@example.com",
            password="testpassword"
        )
    
    def test_reporter_creation(self):
        """Test creating a reporter profile"""
        reporter = Reporter.objects.create(
            user=self.user,
            bio="Test reporter bio"
        )
        self.assertEqual(str(reporter), "Test User")
        self.assertEqual(reporter.bio, "Test reporter bio")


class ArticleModelTest(TestCase):
    """Test cases for the Article model"""
    
    def setUp(self):
        """Set up test data"""
        # Create user and reporter
        self.user = User.objects.create_user(
            username="reporter",
            first_name="Jane",
            last_name="Doe",
            password="password123"
        )
        self.reporter = Reporter.objects.create(user=self.user)
        
        # Create category
        self.category = Category.objects.create(name="Sports")
        
        # Create tags
        self.tag1 = Tag.objects.create(name="Football")
        self.tag2 = Tag.objects.create(name="World Cup")
    
    def test_article_creation(self):
        """Test creating an article with relationships"""
        article = Article.objects.create(
            title="Test Article",
            content="This is test content for the article.",
            reporter=self.reporter,
            category=self.category,
            status="published"
        )
        
        # Add tags
        article.tags.add(self.tag1, self.tag2)
        
        # Test basic properties
        self.assertEqual(article.title, "Test Article")
        self.assertEqual(article.slug, "test-article")
        self.assertEqual(str(article), "Test Article")
        
        # Test relationships
        self.assertEqual(article.reporter, self.reporter)
        self.assertEqual(article.category, self.category)
        self.assertEqual(article.tags.count(), 2)
        self.assertTrue(self.tag1 in article.tags.all())
        self.assertTrue(self.tag2 in article.tags.all())
        
        # Test summary generation
        self.assertTrue(article.summary.startswith("This is test content"))


class ArticleViewTests(TestCase):
    """Test cases for article views"""
    
    def setUp(self):
        """Set up test data"""
        # Create user and reporter
        self.user = User.objects.create_user(
            username="testuser", 
            password="testpass123"
        )
        self.reporter = Reporter.objects.create(user=self.user)
        
        # Create category
        self.category = Category.objects.create(
            name="Technology",
            description="Tech news and reviews"
        )
        
        # Create articles
        self.article1 = Article.objects.create(
            title="First Test Article",
            slug="first-test-article",
            content="This is the content of the first test article.",
            reporter=self.reporter,
            category=self.category,
            status="published"
        )
        
        self.article2 = Article.objects.create(
            title="Second Test Article",
            slug="second-test-article",
            content="This is the content of the second test article.",
            reporter=self.reporter,
            category=self.category,
            status="published"
        )
        
        # Create draft article
        self.draft_article = Article.objects.create(
            title="Draft Article",
            slug="draft-article",
            content="This is a draft article.",
            reporter=self.reporter,
            category=self.category,
            status="draft"
        )
    
    def test_home_view(self):
        """Test the home page view"""
        response = self.client.get(reverse("news:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "news/home.html")
        self.assertContains(response, "First Test Article")
        self.assertContains(response, "Second Test Article")
        self.assertNotContains(response, "Draft Article")  # Draft should not appear
    
    def test_article_detail_view(self):
        """Test the article detail view"""
        response = self.client.get(
            reverse("news:article_detail", args=[self.article1.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "news/article_detail.html")
        self.assertContains(response, "First Test Article")
        self.assertContains(response, "This is the content")
    
    def test_category_view(self):
        """Test the category detail view"""
        response = self.client.get(
            reverse("news:category_detail", args=[self.category.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "news/category_detail.html")
        self.assertContains(response, "Technology")
        self.assertContains(response, "First Test Article")
        self.assertContains(response, "Second Test Article")
