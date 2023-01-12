---
title: Sudowoodo reminding you to be careful when using sudo
date: 2020-01-20
slug: sudowoodo-sudo
---
Remember the lecture that you received when you first used sudo?

<pre class="synNormal">
We trust you have received the usual lecture from the local System Administrator.
It usually boils down to these three things:

    #1) Respect the privacy of others.
    #2) Think before you type.
    #3) With great power comes great responsibility.
</pre>

It's a pretty nice warning, unfortunately, it only appears once. You can edit the sudoers file to make it permanent. Open the fine by running `sudo visudo` and then modify it to have the following line.

<pre class="synNormal">
Defaults    lecture=always
</pre>

You can also set a custom lecture, for instance, an [ascii image of sudowoodo](https://github.com/0aax/sudowoodo/blob/master/sudoers.lecture). Create a new file with the message to be displayed and set `lecture_file` to wherever the file is (e.g. `/etc/sudoers.lecture`).

<pre class="synNormal">
# (replace the path with your own)
Defaults    lecture_file=/etc/sudoers.lecture
</pre>