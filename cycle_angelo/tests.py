from django.test import TestCase
from cycle_angelo.models import Post
from django.urls import reverse

# Create your tests here.

class CategoryMethodTests(TestCase):
    
    def test_ensure_view_are_positive(self):
        """
        Ensures the number of views received for a Category are positive or zero
        """
        category = Category(name='test', views=-1, likes=0)
        category.save()

        self.assertEqual((category.views >= 0), True)



    def test_slug_line_creation(self):
        """
        Checks to make sure that when a post is created, an appropriate slug
        is created.
        """
        post = Post(title = "I love bikes", content = "Bikes are great")
        post.save()

        self.assertEqual(post.slug, 'i-love-bikes')


class IndexViewTests(TestCase):
    def test_index_view_with_no_posts(self):
        """
        If no posts exist, the appropriate message should be displayed.
        """
        response = self.client.get(reverse('cycle_angelo:index'))

        self.assertEqual(response.status_code, 200)
        #self.assertContains(response, 'There are no posts present.')
        self.assertQuerysetEqual(response.context['posts'], [])

    def test_add_post(self):
        """
        Checks to make sure posts can be added and displayed on the index page
        """
        post = Post.objects.get_or_create(title=title)[0]
        post.content = content

        post.save()
        response = self.client.get(reverse('cycle_angelo:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, title)
        self.assertQuerysetEqual(reponse.context['posts'], [title])


    def test_index_view_with_posts(self):
        """
        Checks whether posts are displayed correctly when present
        """
        add_post('I love bikes', 'Bikes are great')
        add_post('Great ride this morning', "Lovely ride along the Kelvin")

        response = self.client.get(reverse('cycle_angelo:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "I love bikes")
        self.assertContains(repsonse, "Great ride this morning")

        num_posts = len(repsonse.context['posts'])
        self.assertEquals(num_posts, 2)

def add_post(title, content):
    post = Post.objects.get_or_create(title=title)[0]
    post.content = content

    post.save()
    return post
