import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WAD2_team_exercise.settings')

import django
django.setup()

from django.test import TestCase
from cycle_angelo.models import Post, User, Comment, UserProfile
from django.urls import reverse
import random


# Create your tests here.

####### Helper functions #########
random.seed(485309)
def add_post(content, name, title='', comments=0):

    creator = User(username=name)
    if not creator.DoesNotExist:
        creator = User(random.randint(1,1000))
    creator.save()
    post = Post.objects.get_or_create(title=title, content=content,
                                    creator=creator, number_of_comments=comments)[0]
    post.save()
    if comments > 0:
        for i in range(comments):
            comm = random.randint(1, 1000)
            add_comment(post, comm)
    return post

def add_comment(post, content):
    creator = User(username=random.randint(1,1000))
    if not creator.DoesNotExist:
        creator = User(random.randint(1,1000))
    creator.save()
    c = Comment.objects.get_or_create(post=post, content=content, user=creator)[0]
    c.save()
    return c

####### Testing Classes ########

class IndexViewTests(TestCase):
    '''
    test if displays proper posts
    posts with most comments
    recent posts
    hyperlinks work
    '''
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
        add_post('I love bikes', 'Bikes are great', 'Lucas')
        add_post('Great ride this morning', "Lovely ride along the Kelvin", 'Adam')

        response = self.client.get(reverse('cycle_angelo:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "I love bikes")
        self.assertContains(response, "Great ride this morning")

        num_posts = len(response.context['new_posts'])
        self.assertEquals(num_posts, 2)

    def test_top_five_posts(self):
        '''
        Checks to make sure the top posts are ordered correctly by number of
        comments
        '''
        add_post(title='I love bikes', content='Bikes are great', name='Lucas', comments=10)
        add_post(title='Morning!', content='Lovely ride along the Kelvin', name='Adam', comments=2)
        add_post(title='Biking', content='good places to ride?', name='Nile', comments=5)
        add_post(title='Gears', content='need new gears', name='HamishC', comments=1)
        add_post(title='Howdy!', content='Wrong app!', name='Rango', comments=7)

        rankings = ['<Post: I love bikes>', '<Post: Howdy!>', '<Post: Biking>',
                    '<Post: Morning!>', '<Post: Gears>']

        response = self.client.get(reverse('cycle_angelo:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['top_posts'], rankings)

    def test_five_new_posts(self):
        '''
        Checks to make sure the order of the new posts are being shown correctly
        '''
        add_post(title='I love bikes', content='Bikes are great', name='Lucas')
        add_post(title='Morning!', content='Lovely ride along the Kelvin', name='Adam')
        add_post(title='Biking', content='good places to ride?', name='Nile')
        add_post(title='Gears', content='need new gears', name='HamishC')
        add_post(title='Howdy!', content='Wrong app!', name='Rango')

        rankings = ['<Post: Howdy!>', '<Post: Gears>', '<Post: Biking>',
                    '<Post: Morning!>', '<Post: I love bikes>']

        response = self.client.get(reverse('cycle_angelo:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['new_posts'], rankings)




class ShowPostViewTests(TestCase):
    '''
    test to make sure Posts are shown correctly
    check for with and without title
    check content is present
    check comments
    '''

    def test_post_no_title(self):
        post = add_post(content="hello", name='Lucas')
        url = reverse('cycle_angelo:show_post', args=(post.slug,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['post'], post)


    def test_post_with_title(self):
        post = add_post(content="hello", name='Lucas',  title='hiya')
        url = reverse('cycle_angelo:show_post', args=(post.slug,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['post'], post)

    def test_post_with_comments(self):
        post = add_post(content="hello", name='Lucas', comments = 5)
        url = reverse('cycle_angelo:show_post', args=(post.slug,))
        response = self.client.get(url)

        num_comments = len(response.context['comments'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(num_comments, 5)

    def test_post_slug_no_title(self):
        post = add_post(content="Hi I'm new here!", name='Lucas')
        url = reverse('cycle_angelo:show_post', args=(post.slug,))
        response = self.client.get(url)

        self.assertEqual(url, "/cycle_angelo/post/hi-im-new-here/")

    def test_post_slug_with_title(self):
        post = add_post(content="Hi I'm new here!", name='Lucas', title="hiya")
        url = reverse('cycle_angelo:show_post', args=(post.slug,))
        response = self.client.get(url)

        self.assertEqual(url, "/cycle_angelo/post/hi-im-new-here/")



class ProfileViewTests(TestCase):
    '''
    Testing for viewing the ProfileView
    '''

    def test_profile_page_accessible(self):
        profile=User(username='Boris')
        profile.save()
        name = profile.get_username()
        url = reverse('cycle_angelo:profile', args=(name,))
        response = self.client.get(url)

        self.assertURLEqual(url, "/cycle_angelo/profile/Boris/")
