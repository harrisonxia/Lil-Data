module.exports = {
    "verbose": true,
    "moduleFileExtensions": [
        "js",
        "jsx"
    ],
    "moduleDirectories": [
        "node_modules",
        "src"
    ],
    "globals": {
        "__DEV__": false,
    },
    testPathIgnorePatterns: [
        "/node_modules/",
        "/dist/",
        "/dist-server/"
    ],
    rootDir: ".."
};