-- Game versions
---Default target version for unknown builds and builds created before 3.0.0.
legacyTargetVersion = "1_1"
---Default target for new builds and target to convert legacy builds to.
liveTargetVersion = "1_1"

-- Skill tree versions
---Added for convenient indexing of skill tree versions.
---@type string[]
treeVersionList = { "1_1", }
--- Always points to the latest skill tree version.
latestTreeVersion = treeVersionList[#treeVersionList]
---Tree version where multiple skill trees per build were introduced to PoBC.
defaultTreeVersion = treeVersionList[2]
---Display, comparison and export data for all supported skill tree versions.
---@type table<string, {display: string, num: number, url: string}>
treeVersions = {
	["1_1"] = {
		display = "1.1",
		num = 1.1,
		url = "",
	},
}
