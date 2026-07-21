module.exports = {
    preset: [
        ['@babel/preset-env', {
            targets: {
                safari: '12',
                macos: '12'
            },
            useBuiltIns: 'entry',
            corejs: 3
        }]
    ]
}