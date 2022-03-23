from django.test import TestCase
from cycle_angelo.models import Post
from django.urls import reverse

# Create your tests here.


class IndexViewTests(TestCase):
    def test_index_view_with_no_posts(self):
        """
        If no posts exist, the page should just be empty.
        """
        response = self.client.get(reverse('cycle_angelo:index'))

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['new_posts'], [])
        self.assertQuerysetEqual(response.context['top_posts'], [])


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

def add_post(title, content, likes=0):
    post = Post.objects.get_or_create(title=title)
    post.content = content
    post.likes = likes

    post.save()
    return post
