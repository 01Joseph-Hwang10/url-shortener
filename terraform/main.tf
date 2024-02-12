# ---------------------------
# Github
# ---------------------------
resource "github_repository" "url_shortener" {
  name            = "url-shortener"
  visibility      = "public"
  has_issues      = true
  has_projects    = true
  has_downloads   = true
  has_discussions = false
  has_wiki        = false
}
