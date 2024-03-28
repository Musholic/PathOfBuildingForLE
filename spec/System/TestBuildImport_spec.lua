it("build import from LETools #buildImport", function()
    newBuild()
    local jsonFile = io.open("../spec/System/letools_import.json", "r")
    local importCode = jsonFile:read("*a")
    jsonFile:close()
    print(importCode)
    build:Init(false, "Imported build", importCode)
    runCallback("OnFrame")
    assert.are.equals(1251, build.calcsTab.calcsOutput.Life)
end)