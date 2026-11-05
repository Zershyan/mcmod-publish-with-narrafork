/**
 * 构建前确认：填 mod_version、选要发布的分支。
 * 只用于装了 zershyan-mcmod-style 的工程；提交后由用户自己跑构建。
 * 复制本文件与 data.ts 到 .narrafork/gen_ui/<名称>/ 后 show 该目录。
 */
import { useState } from "react";
import {
	Alert,
	Badge,
	Box,
	Button,
	Card,
	Group,
	MultiSelect,
	Stack,
	Text,
	TextInput,
	Title,
} from "@mantine/core";
import { DATA } from "./data";

type FormData = {
	projectName: string;
	/** 当前工程的 mod_version，作为初始值 */
	currentVersion: string;
	/** git 分支列表 */
	branches: string[];
	/** 默认勾选的分支 */
	defaultBranches?: string[];
	/** 提示信息 */
	hints?: string[];
};

const D = DATA as FormData;

export default function App() {
	const [version, setVersion] = useState(D.currentVersion);
	const [branches, setBranches] = useState<string[]>(D.defaultBranches ?? []);

	const ready = version.trim().length > 0 && branches.length > 0;

	const submit = () => {
		(globalThis as any).genUI?.submit(
			{ modVersion: version.trim(), branches },
			`按 ${version.trim()} 构建 ${branches.join('、')}`,
		);
	};

	return (
		<Box p="lg">
			<Stack gap={2} mb="md">
				<Title order={3}>发布前确认</Title>
				<Text size="sm" c="dimmed">
					{D.projectName}
				</Text>
			</Stack>

			<Card withBorder shadow="sm" radius="md" p="md" mb="md">
				<Stack gap="sm">
					<TextInput
						label="版本号（mod_version）"
						description="只写模组版本，不要带 MC 版本或 build 编号"
						placeholder="0.0.1"
						value={version}
						onChange={(e) => setVersion(e.currentTarget.value)}
					/>
					<MultiSelect
						label="要发布的分支"
						description="每个分支单独构建、单独上传"
						data={D.branches}
						value={branches}
						onChange={setBranches}
						placeholder="选择分支"
						clearable
					/>
				</Stack>
			</Card>

			{D.hints?.length ? (
				<Alert color="blue" title="接下来" mb="md">
					<ul style={{ margin: 0, paddingLeft: 18 }}>
						{D.hints.map((item) => (
							<li key={item}>{item}</li>
						))}
					</ul>
				</Alert>
			) : (
				<Alert color="blue" title="接下来" mb="md">
					<Text size="sm">
						提交后请自己在各分支上运行 <code>./gradlew build</code>，完成后告诉我。
						我会用 <code>build/libs</code> 里不带 build 编号的 jar 继续。
					</Text>
				</Alert>
			)}

			<Group justify="space-between" align="center">
				<Group gap="xs">
					<Badge variant="light">{branches.length} 个分支</Badge>
					{branches.map((b) => (
						<Badge key={b} size="sm" variant="default" tt="none">
							{b}
						</Badge>
					))}
				</Group>
				<Button onClick={submit} disabled={!ready} radius="md">
					确认
				</Button>
			</Group>
		</Box>
	);
}
