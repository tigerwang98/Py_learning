// 将js代码转换为ast对象
const parser = require("@babel/parser");
// 在节点遍历或者其他操作中做类型判断或者类型转换
const types = require("@babel/types");
// 将ast对象转换为js代码
const generator = require("@babel/generator");
// 能够遍历ast节点树并对其中的节点进行操作
const traverse = require("@babel/traverse");
// 一些复杂的代码可以直接通过template进行操作(增删改查等)
const template = require("@babel/template");

var code = `
    function add(a,b) {
        if((a+b) < 10) {
            console.log('两个数之和小于10!');
        }
        else if(10 <= (a+b) < 20) {
            return a+b;
        }
        else {
            console.log('两个数之和大于20');
        }
    }
`
const ast = parser.parse(code);

function handleAst() {
    const visitor = {
        // 语法树中的哪一个node
        StringLiteral(path) {
            const node = path.node;
            if(node.value === "两个数之和大于20") {
                node.value = '我已经修改啦!哈哈!';
            }
        }
    }
    traverse.default(ast, visitor);
}

function addNewNode() {
    const visitor = {
        ReturnStatement(path) {
            const node = path.node;
            if(types.isNumericLiteral(node.argument)) {
                var newNode = template.default('console.log(a+b)')();
                path.insertBefore(newNode);
            }
        }
    }
    traverse.default(ast, visitor)
    const finalCode = generator.default(ast).code;
    console.log('===============')
    console.log(finalCode);
}


handleAst()
const newCode = generator.default(ast).code;
console.log(newCode);