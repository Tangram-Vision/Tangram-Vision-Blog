# Contributing to Tangram Vision OSS

Thanks for contributing!

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md), adapted from the Contributor Covenant v2.0. By participating in this project you agree to abide by its terms.

Tangram Vision hosts all of its Open-source Software (OSS) on both GitLab and GitHub. We do this for accessibility's sake. However, these repositories are maintained in GitLab; all bugs and contributions should therefore be made through GitLab.

Visit the [repository homepage on GitLab here](https://gitlab.com/tangram-vision-oss/realsense-rust).

## tl;dr

- Use the GitLab repository (above) to submit issues and merge requests.
- Check the documentation.
- Bugs and enhancements should be categorized and explained to the best of the submitter's ability; guidelines below.
- Merge Requests must pass unit and integration tests before accepted.
- Follow our commit message guidelines.
- Follow the Code of Conduct.

## Bugs

Before submitting a bug report, we encourage you to read the documentation. We pride ourselves on good documentation and explanation; if we've hit something strange or annoying, the odds are high that it's been documented.

If the documentation doesn't help, search existing issues. Make sure that your issue hasn't been logged already. If nothing shows, it's time to report a bug!

All bug reports are tracked in the repository's GitLab Issues. Good bug reports have several elements that can help the maintainers better understand the issue:

- Exact steps taken to reproduce the problem: Describe the operating system in use at the time, and any hardware/firmware that you were running with the module when it glitched. Code snippets that demonstrate the bug are valuable.
- A description of the desired vs observed behavior: Explain how the outcome of your program didn't match expectations.
- Screenshots: if applicable. Pictures of words are worth... words, too? They help. Don't look too much into it.
- A description of your work environment: this can be helpful if your setup is customized in any way.

## Enhancements

Enhancements desecribe new features or quality-of-life improvements that would make the software experience better.

Before submitting an enhancement, we encourage you to read the documentation. The feature you'd like to see might already be implemented! If this is the case, it's not the code that should be improved; it's the documentation (something that can also be reported as an enhancement).

All proposed enhancements are logged using GitLab Issues. Good enhancement suggestions have the following parts:

- A summary of the enhancement: Describe the goal of the modification. Ease of use? More functionality? Compatibility? Be as descriptive as possible.
- The motivation behind the suggestion: This enhancement might save you time, or memory, or brain power.
- How this is done now: What steps do you have to take to meet your goals without the enhancement in place? If there is no alternative, how will this enhancement help?

## Code Contributions

We're excited that you're excited to contribute! Excitement all around, really.

If you are a first-time contributor, we encourage you to look at the open Issues and start there. Accessible Issues should be labeled as such for those looking to jump into the mix.

We at Tangram are meticulous about our Continuous Integration (CI) practices. Anything we can automate, we can! This includes code lint runs, documentation checks, and unit testing across all files. Similarly, contributions will have to follow good CI:

- Bug fixes and new functionality should include new unit and integration tests demonstrating its validity and use.
- All MRs must pass the Tangram testing suite before they are eligible for merge.
- Note clearly in the MR if hardware is required for testing. We will not merge a request until this testing is verified as passing.

You should be able to run all these tests from the comfort of your own machine. These steps will usually be described in a TESTING.md in the top directory.

## Commit messages

Commit messages are the number one way of communicating intent and context across a project. If you have a well-organized history, it is fairly straightforward to ascertain the context behind why code is written the way it is. From this, it is usually much easier to fix a bug, or get in the mindset of whoever wrote the code you're looking at (even if that person is you). [This article](https://chris.beams.io/posts/git-commit/) by Chris Beams does a good job explaining this philosophy.

The subject line of a commit message is the *what*, and the body is the *why*.

### Seven guidelines for a good commit message:

1. [Separate subject from body with a blank line](https://chris.beams.io/posts/git-commit/#separate)
2. [Limit the subject line to 50 characters](https://chris.beams.io/posts/git-commit/#limit-50)
3. [Capitalize the subject line](https://chris.beams.io/posts/git-commit/#capitalize)
4. [Do not end the subject line with a period](https://chris.beams.io/posts/git-commit/#end)
5. [Use the imperative mood in the subject line](https://chris.beams.io/posts/git-commit/#imperative)
6. [Wrap the body at 72 characters](https://chris.beams.io/posts/git-commit/#wrap-72)
7. [Use the body to explain *what* and *why* vs. *how*](https://chris.beams.io/posts/git-commit/#why-not-how)

