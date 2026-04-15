diff --git a/build.sh b/build.sh
new file mode 100755
index 0000000..1111111
--- /dev/null
+++ b/build.sh
@@ -0,0 +1,17 @@
+#!/usr/bin/env bash
+set -o errexit
+
+# Install dependencies
+pip install -r requirements.txt
+
+# Collect static files (required for production static serving patterns)
+python manage.py collectstatic --no-input
+
+# Apply database migrations
+python manage.py migrate
