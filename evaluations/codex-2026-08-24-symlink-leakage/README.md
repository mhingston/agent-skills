# Harness audit: invalid baseline run

These records are preserved for audit only and must not be used as behavioural
evidence. The first fixture builder exposed skill packages as symlinks into the
source checkout. A baseline run followed an absolute source path and loaded the
skill that was supposed to be omitted, so the baseline was not isolated. The
canonical rerun uses copied skill directories with no source-tree symlinks.
