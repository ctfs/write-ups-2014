# ECTF 2014: Eight Cats Hid the Flag

**Category:** Recon
**Points:** 100
**Description:**

> Find the flag.
>
> **Hint:** Have you learnt a version control system before? Because one of our team members says he has.

## Write-up

“Eight cats” is a hint at [Octocat, the official GitHub mascot](https://octodex.github.com/). We probably have to look for the flag on one of the CTF organizer’s GitHub repositories.

Cloning all of @karthiksenthil’s repositories and `grep`ping for a flag yields no results. There seems to be no other way of finding the flag except manually going through all commits, as the flag has been deleted from the source code. The commit in question was made a month before the CTF started, which made things a bit more difficult. By manually looking through all the commits we eventually found commit https://github.com/karthiksenthil/Learn-Git/commit/9cd4ecad6f7c545ef5ac31622d503de811191d7b which contains the flag `flag{0ctocat_c4n_play_h1de_and_s33k}`.

### Alternate solution

By searching the commit messages for the word “flag” the correct commit can quickly be found:

```bash
$ git clone https://github.com/karthiksenthil/Learn-Git && cd Learn-Git
Cloning into 'Learn-Git'...
remote: Counting objects: 1926, done.
remote: Compressing objects: 100% (984/984), done.
Rceiving objects:  66% (1272/1926), 916.00 KiB | 404.00 KiB/s
remote: Total 1926 (delta 863), reused 1926 (delta 863)
Receiving objects: 100% (1926/1926), 2.91 MiB | 576.00 KiB/s, done.
Resolving deltas: 100% (863/863), done.
Checking connectivity... done.
No submodule mapping found in .gitmodules for path 'courses/2'

$ git log --grep=flag
commit 9cd4ecad6f7c545ef5ac31622d503de811191d7b
Author: Karthik Senthil <karthik.senthil94@gmail.com>
Date:   Sat Sep 20 15:55:20 2014 +0530

    Removed flag :O

$ git show 9cd4ecad6f7c545ef5ac31622d503de811191d7b
commit 9cd4ecad6f7c545ef5ac31622d503de811191d7b
Author: Karthik Senthil <karthik.senthil94@gmail.com>
Date:   Sat Sep 20 15:55:20 2014 +0530

    Removed flag :O

diff --git a/LICENSE b/LICENSE
index 2200a82..89508a9 100644
--- a/LICENSE
+++ b/LICENSE
@@ -18,4 +18,3 @@ LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 THE SOFTWARE.

-flag{0ctocat_c4n_play_h1de_and_s33k}
```

## Other write-ups and resources

* <http://dhanvi1.wordpress.com/2014/10/23/eight-cats-hid-the-flag-ectf-2014-recon-100-writeup/>
