# Search ranking at Shopwise (made up)

#### SRC-S1 · The whole story
`S` · performance, hardest problem · ~25 s
- EN: At Shopwise, search took two seconds at peak, and people left the page. I profiled the ranking service myself and found that we loaded every product before we filtered. I moved the filter into the index query and shipped it behind a flag. Peak latency fell to 300 milliseconds, and searches that ended in a cart grew by 6%.

#### SRC-O1 · First line
`O` · performance · ~5 s
- EN: At Shopwise, search took two seconds at peak, and people left the page.
