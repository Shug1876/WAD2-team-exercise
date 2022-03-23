import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WAD2_team_exercise.settings')

import django
django.setup()

from django.test import TestCase
from cycle_angelo.models import Post, User
from django.urls import reverse

# Create your tests here.


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
        add_post('I love bikes', 'Bikes are great', 'Lucas', 10)
        add_post('Morning!', 'Lovely ride along the Kelvin', 'Adam', 2)
        add_post('Biking', 'good places to ride?', 'Nile', 5)
        add_post('Gears', 'need new gears', 'Hamish', 1)
        add_post('Howdy!', 'Wroong app!', 'Rango', 7)

        rankings = ['<Post: I love bikes>', '<Post: Howdy!>', '<Post: Biking>',
                    '<Post: Morning!>', '<Post: Gears>']

        response = self.client.get(reverse('cycle_angelo:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['top_posts'], rankings)

    def test_five_new_posts(self):
        '''
        Checks to make sure the order of the new posts are being shown correctly
        '''
        add_post('I love bikes', 'Bikes are great', 'Lucas', 10)
        add_post('Morning!', 'Lovely ride along the Kelvin', 'Adam', 2)
        add_post('Biking', 'good places to ride?', 'Nile', 5)
        add_post('Gears', 'need new gears', 'Hamish', 1)
        add_post('Howdy!', 'Wroong app!', 'Rango', 7)

        rankings = ['<Post: Howdy!>', '<Post: Gears>', '<Post: Biking>',
                    '<Post: Morning!>', '<Post: I love bikes>']

        response = self.client.get(reverse('cycle_angelo:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['new_posts'], rankings)


def add_post(title, content, name, comments=0):
    creator = User(username=name)
    creator.save()
    post = Post.objects.get_or_create(title=title, content=content,
                                    creator=creator, number_of_comments=comments)[0]
    post.save()
    return post


class AddPostViewTests(TestCase):
    '''
    test to make sure Posts can be added properly
    check for with and without title
    check content is present
    if photos work
    slug?
    '''

    pass

class AddCommentViewTests(TestCase):
    '''
    tests to see if adding comments works
    empty comments

    '''
