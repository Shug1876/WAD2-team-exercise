import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WAD2_team_exercise.settings')

import django
django.setup()

from cycle_angelo.models import User, Post, Comment

def populate():
    
    post1_comments = [{'content' : 'Nice ride!'}, {'content' : 'Wow that was fast!'}]
    post2_comments = [{'content' : 'How much did that cost?!'}, {'content' : 'Ready to race you soon!'}]
    post3_comments = [{'content' : 'If you add intervals to training that might help'}, {'content' : 'Make sure to sleep enough'}]
    
    test_blogPosts = {'What a day to go out in the bike! 80k\'s in the bank.' : {'comments':post1_comments},
                       'New bike day, ready for some miles in the summer!' : {'comments':post2_comments},
                       'Wanting to stay motivated and get better on the bike. Any ideas?' : {'comments':post3_comments}}
                       
    
    for blogPost, comments in test_blogPosts.items():
        bp = add_post(blogPost)
        for c in comments['comments']:
            add_comment(bp, c['content'])
    
    
    for bp in Post.objects.all():
        for c in Comment.objects.filter(post=bp):
            print(f'- {bp} : {c}')
    
    
def add_post(bp):

    content = bp
    bp = Post.objects.get_or_create(content=content)[0]
    bp.save()
    return bp
    
def add_comment(bp, content):
    c = Comment.objects.get_or_create(post=bp, content=content)[0]
    c.save()
    return c
    
    
if __name__ == '__main__':
    print('Starting Cycle Angelo population script...')
    populate()
    
    