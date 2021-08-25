// ��js����ת��Ϊast����
const parser = require("@babel/parser");
// �ڽڵ�������������������������жϻ�������ת��
const types = require("@babel/types");
// ��ast����ת��Ϊjs����
const generator = require("@babel/generator");
// �ܹ�����ast�ڵ����������еĽڵ���в���
const traverse = require("@babel/traverse");
// һЩ���ӵĴ������ֱ��ͨ��template���в���(��ɾ�Ĳ��)
const template = require("@babel/template");

var code = `
    function add(a,b) {
        if((a+b) < 10) {
            console.log('������֮��С��10!');
        }
        else if(10 <= (a+b) < 20) {
            return a+b;
        }
        else {
            console.log('������֮�ʹ���20');
        }
    }
`
const ast = parser.parse(code);

function handleAst() {
    const visitor = {
        // �﷨���е���һ��node
        StringLiteral(path) {
            const node = path.node;
            if(node.value === "������֮�ʹ���20") {
                node.value = '���Ѿ��޸���!����!';
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