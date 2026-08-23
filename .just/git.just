# Clean up local branches that are merged into the default branch or whose remote is gone
[doc("Clean up local branches that are merged into the default branch or whose remote is gone.")]
[group("Local")]
git-cleanup:
    #!/usr/bin/env bash
    set -euo pipefail

    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    BLUE='\033[0;34m'
    MAGENTA='\033[0;35m'
    CYAN='\033[0;36m'
    BOLD='\033[1m'
    NC='\033[0m'

    echo ""
    echo -e "${BOLD}${CYAN}🧹 Git Branch Cleanup${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""

    if git show-ref --verify --quiet refs/heads/main; then
        DEFAULT_BRANCH="main"
    elif git show-ref --verify --quiet refs/heads/master; then
        DEFAULT_BRANCH="master"
    else
        echo -e "${RED}✗ Error: Could not find 'main' or 'master' branch.${NC}"
        exit 1
    fi

    echo -e "${BLUE}ℹ${NC} Default branch: ${BOLD}$DEFAULT_BRANCH${NC}"
    echo ""

    echo -e "${BLUE}ℹ${NC} Fetching and pruning remote..."
    git fetch --prune
    echo ""

    MERGED_BRANCHES=$(git branch --merged "$DEFAULT_BRANCH" | grep -v "^\*\|^\s*${DEFAULT_BRANCH}$" || true)
    GONE_BRANCHES=$(git branch -vv | grep ': gone]' | awk '{print $1}' || true)

    BRANCHES=$(echo -e "${MERGED_BRANCHES}\n${GONE_BRANCHES}" | grep -v '^$' | sort -u || true)

    if [ -z "$BRANCHES" ]; then
        echo -e "${GREEN}✓ No merged branches to clean up. All tidy!${NC}"
        echo ""
        exit 0
    fi

    BRANCH_COUNT=$(echo "$BRANCHES" | wc -l | tr -d ' ')

    echo -e "${YELLOW}⚠${NC} Found ${BOLD}${BRANCH_COUNT}${NC} branch(es) merged into ${BOLD}$DEFAULT_BRANCH${NC}:"
    echo ""
    echo -e "${MAGENTA}┌──────────────────────────────────────────┐${NC}"
    echo "$BRANCHES" | while read -r branch; do
        echo -e "${MAGENTA}│${NC}  ${RED}✗${NC} $branch"
    done
    echo -e "${MAGENTA}└──────────────────────────────────────────┘${NC}"
    echo ""

    read -p "$(echo -e "${BOLD}Delete these branches? ${NC}[${GREEN}y${NC}/${RED}n${NC}]: ")" CONFIRM

    case "$CONFIRM" in
        y|Y|yes|YES)
            echo ""
            echo -e "${CYAN}Deleting branches...${NC}"
            echo "$BRANCHES" | xargs git branch -D
            echo ""
            echo -e "${GREEN}✓ Done! Removed ${BOLD}${BRANCH_COUNT}${NC}${GREEN} merged branch(es).${NC}"
            echo ""
            ;;
        *)
            echo ""
            echo -e "${BLUE}ℹ${NC} Aborted. No branches were deleted."
            echo ""
            ;;
    esac
