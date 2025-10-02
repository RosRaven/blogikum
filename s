[1mdiff --git a/blogicum/blog/views.py b/blogicum/blog/views.py[m
[1mindex 4c934d3..b311b5b 100644[m
[1m--- a/blogicum/blog/views.py[m
[1m+++ b/blogicum/blog/views.py[m
[36m@@ -1,3 +1,4 @@[m
[32m+[m[32mfrom django.http import Http404[m
 from django.contrib.auth import get_user_model [m
 from django.contrib.auth.decorators import login_required[m
 from django.db.models import Count[m
[36m@@ -348,19 +349,17 @@[m [mdef add_comment(request, post_id):[m
 [m
 @login_required[m
 def edit_comment(request, post_id, comment_id):[m
[31m-    post = get_object_or_404(Post, id=post_id)[m
[32m+[m[32m    """Редактирование комментария."""[m
[32m+[m[32m    post = get_object_or_404(Post, pk=post_id)[m
     comment = get_object_or_404([m
[31m-        Comment.objects.select_related("post", "author"),[m
[31m-        id=comment_id, post=post, author=request.user[m
[31m-    )[m
[31m-    if request.method == "POST":[m
[31m-        form = CommentForm(request.POST, instance=comment)[m
[31m-        if form.is_valid():[m
[31m-            form.save()[m
[31m-            return redirect("blog:post_detail", post_id=post.id)[m
[31m-    else:[m
[31m-        form = CommentForm(instance=comment)[m
[31m-[m
[32m+[m[32m        Comment,[m
[32m+[m[32m        pk=comment_id, post=post)[m
[32m+[m[32m    if comment.author != request.user:[m
[32m+[m[32m        raise Http404[m
[32m+[m[32m    form = CommentForm(request.POST or None, instance=comment)[m
[32m+[m[32m    if request.method == "POST" and form.is_valid():[m
[32m+[m[32m        form.save()[m
[32m+[m[32m        return redirect("blog:post_detail", post_id=post.id)[m
     context = {[m
         "form": form, [m
         "post": post, [m
[36m@@ -370,11 +369,18 @@[m [mdef edit_comment(request, post_id, comment_id):[m
 [m
 [m
 @login_required[m
[31m-# @require_POST[m
 def delete_comment(request, post_id, comment_id):[m
[31m-    post = get_object_or_404(Post, id=post_id)[m
[32m+[m[32m    """Удаление комментария."""[m
[32m+[m[32m    post = get_object_or_404(Post, pk=post_id)[m
     comment = get_object_or_404([m
[31m-        Comment, id=comment_id, post=post, author=request.user[m
[31m-    )[m
[31m-    comment.delete()[m
[31m-    return redirect("blog:post_detail", post_id=post.id)[m
[32m+[m[32m        Comment, pk=comment_id, post=post)[m
[32m+[m[32m    if comment.author != request.user:[m
[32m+[m[32m        raise Http404[m
[32m+[m[32m    if request.method == "POST":[m
[32m+[m[32m        comment.delete()[m
[32m+[m[32m        return redirect("blog:post_detail", post_id=post.id)[m
[32m+[m[32m    context = {[m
[32m+[m[32m            "post": post,[m[41m [m
[32m+[m[32m            "comment": comment,[m
[32m+[m[32m        }[m
[32m+[m[32m    return render(request, "blog/comment.html", context)[m
