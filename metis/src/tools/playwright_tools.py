
from typing import Optional, Dict, Any, List
import asyncio
import base64
import json
import random
from playwright.async_api import async_playwright, Browser, Page
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool

from sanic.log import logger


# 全局 headless 配置，方便调试
PLAYWRIGHT_HEADLESS = False


class PlaywrightManager:
    """Playwright 浏览器和 Page 管理器，单实例多步复用 page"""

    def __init__(self):
        self.playwright = None
        self.browser = None
        self._page = None
        self._lock = asyncio.Lock()

    async def get_browser(self, headless: Optional[bool] = None) -> Browser:
        """获取浏览器实例（内部复用）"""
        # 修正 headless 逻辑，优先参数，其次全局变量，最后默认 True
        if headless is None:
            headless = globals().get("PLAYWRIGHT_HEADLESS", True)
        logger.info(f"get_browser: headless 参数最终值: {headless}")
        need_new_browser = False
        if self.browser is None:
            need_new_browser = True
        else:
            try:
                await self.browser.version()
            except Exception as e:
                logger.warning(f"get_browser: 现有 browser 不可用，需重启: {e}")
                need_new_browser = True
                try:
                    await self.browser.close()
                except Exception as ce:
                    logger.warning(f"get_browser: 关闭旧 browser 失败: {ce}")
                self.browser = None
        if need_new_browser:
            try:
                if self.playwright is None:
                    logger.info("get_browser: 启动 playwright 实例")
                    self.playwright = await async_playwright().start()
                logger.info(
                    f"get_browser: 启动 chromium, headless={headless}")
                # Playwright 1.42+ 需用 chromium.launch() 的 headless 参数为 bool
                self.browser = await self.playwright.chromium.launch(
                    headless=bool(headless),
                    args=[
                        '--no-sandbox',
                        '--disable-dev-shm-usage',
                        '--disable-blink-features=AutomationControlled',
                        '--disable-extensions-except',
                        '--disable-extensions',
                        '--disable-plugins',
                        '--disable-gpu',
                        '--no-first-run',
                        '--no-default-browser-check',
                        '--disable-default-apps',
                        '--disable-popup-blocking',
                        '--disable-translate',
                        '--disable-background-timer-throttling',
                        '--disable-renderer-backgrounding',
                        '--disable-device-discovery-notifications',
                        '--disable-ipc-flooding-protection',
                        '--enable-features=NetworkService,NetworkServiceLogging',
                        '--disable-features=TranslateUI,BlinkGenPropertyTrees',
                        '--window-size=1920,1080'
                    ]
                )
                logger.info("get_browser: Chromium 启动成功")
            except Exception as e:
                logger.error(f"get_browser: Chromium 启动失败: {e}")
                raise
        return self.browser

    async def get_page(self, headless: Optional[bool] = None) -> Page:
        """获取或复用当前 page"""
        if self._page is not None:
            try:
                await self._page.title()  # 检查 page 是否可用
                return self._page
            except Exception:
                try:
                    await self._page.close()
                except:
                    pass
                self._page = None
        browser = await self.get_browser(headless=headless)
        self._page = await browser.new_page()
        return self._page

    async def close_page(self):
        """关闭当前 page"""
        if self._page:
            try:
                await self._page.close()
            except Exception as e:
                logger.warning(f"关闭页面时出现错误: {e}")
            finally:
                self._page = None

    async def close(self):
        """关闭浏览器和 page"""
        if self._page:
            try:
                await self._page.close()
            except Exception as e:
                logger.warning(f"关闭页面时出现错误: {e}")
            finally:
                self._page = None
        if self.browser:
            try:
                await self.browser.close()
            except Exception as e:
                logger.warning(f"关闭浏览器时出现错误: {e}")
            finally:
                self.browser = None
        if self.playwright:
            try:
                await self.playwright.stop()
            except Exception as e:
                logger.warning(f"停止playwright时出现错误: {e}")
            finally:
                self.playwright = None


async def setup_stealth_page(page: Page) -> None:
    """设置页面反爬虫检测"""
    # 设置真实的用户代理
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15'
    ]

    # 设置用户代理
    await page.set_extra_http_headers({
        'User-Agent': random.choice(user_agents)
    })

    # 设置视窗大小（模拟真实用户）
    viewport_sizes = [
        {"width": 1920, "height": 1080},
        {"width": 1366, "height": 768},
        {"width": 1536, "height": 864},
        {"width": 1440, "height": 900}
    ]
    await page.set_viewport_size(random.choice(viewport_sizes))

    # 添加真实浏览器的 JavaScript 属性
    await page.add_init_script("""
        // 覆盖 webdriver 属性
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined,
        });
        
        // 覆盖 plugins 数组
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5],
        });
        
        // 覆盖 languages 属性
        Object.defineProperty(navigator, 'languages', {
            get: () => ['en-US', 'en', 'zh-CN', 'zh'],
        });
        
        // 覆盖 platform 属性
        Object.defineProperty(navigator, 'platform', {
            get: () => 'Win32',
        });
        
        // 模拟真实的 Chrome 运行时
        window.chrome = {
            runtime: {},
            loadTimes: function() {},
            csi: function() {},
            app: {}
        };
        
        // 覆盖权限查询
        const originalQuery = window.navigator.permissions.query;
        window.navigator.permissions.query = (parameters) => (
            parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
        );
        
        // 伪造媒体设备
        Object.defineProperty(navigator, 'mediaDevices', {
            get: () => ({
                enumerateDevices: () => Promise.resolve([
                    { deviceId: 'default', kind: 'audioinput', label: '', groupId: '' },
                    { deviceId: 'default', kind: 'videoinput', label: '', groupId: '' }
                ])
            })
        });
        
        // 移除 Playwright 特征
        delete window.__playwright;
        delete window.__pw_manual;
        delete window.__PW_inspect;
    """)

    # 设置额外的 headers（包含用户代理）
    selected_ua = random.choice(user_agents)
    await page.set_extra_http_headers({
        'User-Agent': selected_ua,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1'
    })


# 全局浏览器管理器
browser_manager = PlaywrightManager()


@tool
async def playwright_get_page_content(
    url: str,
    wait_for: Optional[str] = None,
    timeout: Optional[int] = 30000,
    headless: Optional[bool] = None,
    config: RunnableConfig = None
) -> str:
    """
    获取网页内容
    :param url: 目标网页URL
    :param wait_for: 等待元素选择器 (可选)
    :param timeout: 超时时间 (毫秒，默认30秒)
    :param headless: 是否无头模式 (默认True)
    :return: 网页文本内容
    """
    try:
        page = await browser_manager.get_page(headless=headless)
        # 设置反爬虫检测（只在首次设置）
        if not hasattr(page, '_stealth_inited'):
            await setup_stealth_page(page)
            setattr(page, '_stealth_inited', True)

        await page.goto(url, timeout=timeout, wait_until='domcontentloaded')
        if wait_for:
            await page.wait_for_selector(wait_for, timeout=timeout)
        await page.wait_for_load_state('networkidle', timeout=timeout)
        await page.evaluate("""
            window.scrollTo(0, Math.floor(Math.random() * 500));
            setTimeout(() => window.scrollTo(0, 0), Math.random() * 1000);
        """)
        title = await page.title()
        content = await page.inner_text('body')
        result = f"标题: {title}\n\n内容:\n{content}"
        user_id = config.get('configurable', {}).get(
            'user_id', 'unknown') if config else 'unknown'
        logger.info(f"用户:[{user_id}]执行工具[Playwright 获取页面内容],URL:[{url}]")
        return result
    except Exception as ex:
        logger.error(f"获取页面内容失败: {ex}")
        return f"错误: {str(ex)}"


@tool
async def playwright_screenshot(
    url: str,
    full_page: Optional[bool] = True,
    element_selector: Optional[str] = None,
    timeout: Optional[int] = 30000,
    headless: Optional[bool] = None,
    config: RunnableConfig = None
) -> str:
    """
    网页截图
    :param url: 目标网页URL
    :param full_page: 是否截取整个页面 (默认True)
    :param element_selector: 截取特定元素的选择器 (可选)
    :param timeout: 超时时间 (毫秒，默认30秒)
    :param headless: 是否无头模式 (默认True)
    :return: Base64编码的截图数据
    """
    try:
        page = await browser_manager.get_page(headless=headless)
        if not hasattr(page, '_stealth_inited'):
            await setup_stealth_page(page)
            setattr(page, '_stealth_inited', True)
        await page.goto(url, timeout=timeout, wait_until='domcontentloaded')
        await page.wait_for_load_state('networkidle', timeout=timeout)
        await asyncio.sleep(random.uniform(0.5, 2.0))
        await page.evaluate("window.scrollTo(0, Math.floor(Math.random() * 200));")
        await asyncio.sleep(random.uniform(0.5, 1.0))
        if element_selector:
            element = await page.query_selector(element_selector)
            if element:
                screenshot_bytes = await element.screenshot()
            else:
                raise Exception(f"未找到元素: {element_selector}")
        else:
            screenshot_bytes = await page.screenshot(full_page=full_page)
        base64_image = base64.b64encode(screenshot_bytes).decode('utf-8')
        user_id = config.get('configurable', {}).get(
            'user_id', 'unknown') if config else 'unknown'
        logger.info(f"用户:[{user_id}]执行工具[Playwright 截图],URL:[{url}]")
        return f"data:image/png;base64,{base64_image}"
    except Exception as ex:
        logger.error(f"截图失败: {ex}")
        return f"错误: {str(ex)}"


@tool
async def playwright_fill_form(
    url: str,
    form_data: str,
    submit_selector: Optional[str] = None,
    timeout: Optional[int] = 30000,
    headless: Optional[bool] = None,
    config: RunnableConfig = None
) -> str:
    """
    填写表单
    :param url: 目标网页URL
    :param form_data: 表单数据 JSON字符串 {"selector": "value", ...}
    :param submit_selector: 提交按钮选择器 (可选)
    :param timeout: 超时时间 (毫秒，默认30秒)
    :param headless: 是否无头模式 (默认True)
    :return: 操作结果
    """
    try:
        page = await browser_manager.get_page(headless=headless)
        if not hasattr(page, '_stealth_inited'):
            await setup_stealth_page(page)
            setattr(page, '_stealth_inited', True)
        await page.goto(url, timeout=timeout, wait_until='domcontentloaded')
        await page.wait_for_load_state('networkidle', timeout=timeout)
        try:
            data = json.loads(form_data)
        except json.JSONDecodeError:
            raise Exception("表单数据格式错误，应为有效的JSON字符串")
        filled_fields = []
        for selector, value in data.items():
            try:
                await asyncio.sleep(random.uniform(0.3, 1.0))
                await page.click(selector)
                await asyncio.sleep(random.uniform(0.1, 0.3))
                await page.keyboard.press('Control+KeyA')
                await asyncio.sleep(0.1)
                await page.type(selector, str(value), delay=random.uniform(50, 150))
                filled_fields.append(f"{selector}: {value}")
            except Exception as e:
                logger.warning(f"填写字段 {selector} 失败: {e}")
        if submit_selector:
            await asyncio.sleep(random.uniform(0.5, 1.5))
            await page.click(submit_selector)
            await page.wait_for_load_state('networkidle', timeout=timeout)
            result_msg = "表单已填写并提交"
        else:
            result_msg = "表单已填写 (未提交)"
        user_id = config.get('configurable', {}).get(
            'user_id', 'unknown') if config else 'unknown'
        logger.info(f"用户:[{user_id}]执行工具[Playwright 填写表单],URL:[{url}]")
        return f"{result_msg}\n已填写字段:\n" + "\n".join(filled_fields)
    except Exception as ex:
        logger.error(f"填写表单失败: {ex}")
        return f"错误: {str(ex)}"


@tool
async def playwright_click_and_wait(
    url: str,
    click_selector: str,
    wait_for_selector: Optional[str] = None,
    timeout: Optional[int] = 30000,
    headless: Optional[bool] = None,
    config: RunnableConfig = None
) -> str:
    """
    点击元素并等待响应
    :param url: 目标网页URL
    :param click_selector: 要点击的元素选择器
    :param wait_for_selector: 等待出现的元素选择器 (可选)
    :param timeout: 超时时间 (毫秒，默认30秒)
    :param headless: 是否无头模式 (默认True)
    :return: 操作结果和页面内容
    """
    try:
        page = await browser_manager.get_page(headless=headless)
        if not hasattr(page, '_stealth_inited'):
            await setup_stealth_page(page)
            setattr(page, '_stealth_inited', True)
        await page.goto(url, timeout=timeout, wait_until='domcontentloaded')
        await page.wait_for_load_state('networkidle', timeout=timeout)
        await asyncio.sleep(random.uniform(0.5, 1.5))
        element = await page.query_selector(click_selector)
        if element:
            await element.hover()
            await asyncio.sleep(random.uniform(0.2, 0.5))
        await page.click(click_selector)
        if wait_for_selector:
            await page.wait_for_selector(wait_for_selector, timeout=timeout)
        else:
            await page.wait_for_load_state('networkidle', timeout=timeout)
        title = await page.title()
        content = await page.inner_text('body')
        user_id = config.get('configurable', {}).get(
            'user_id', 'unknown') if config else 'unknown'
        logger.info(
            f"用户:[{user_id}]执行工具[Playwright 点击等待],URL:[{url}],选择器:[{click_selector}]")
        return f"点击成功\n当前页面标题: {title}\n\n页面内容:\n{content}"
    except Exception as ex:
        logger.error(f"点击操作失败: {ex}")
        return f"错误: {str(ex)}"


@tool
async def playwright_get_elements_info(
    url: str,
    selector: str,
    attributes: Optional[str] = "text,href,src,value",
    timeout: Optional[int] = 30000,
    headless: Optional[bool] = None,
    config: RunnableConfig = None
) -> str:
    """
    获取页面元素信息
    :param url: 目标网页URL  
    :param selector: 元素选择器
    :param attributes: 要获取的属性，逗号分隔 (默认: text,href,src,value)
    :param timeout: 超时时间 (毫秒，默认30秒)
    :param headless: 是否无头模式 (默认True)
    :return: 元素信息JSON字符串
    """
    try:
        page = await browser_manager.get_page(headless=headless)
        if not hasattr(page, '_stealth_inited'):
            await setup_stealth_page(page)
            setattr(page, '_stealth_inited', True)
        await page.goto(url, timeout=timeout, wait_until='domcontentloaded')
        await page.wait_for_load_state('networkidle', timeout=timeout)
        await asyncio.sleep(random.uniform(0.5, 1.0))
        elements = await page.query_selector_all(selector)
        if not elements:
            return "未找到匹配的元素"
        attrs = [attr.strip() for attr in attributes.split(',')]
        results = []
        for i, element in enumerate(elements):
            element_info = {"index": i}
            for attr in attrs:
                try:
                    if attr == 'text':
                        element_info[attr] = await element.inner_text()
                    elif attr == 'html':
                        element_info[attr] = await element.inner_html()
                    else:
                        element_info[attr] = await element.get_attribute(attr)
                except Exception as e:
                    element_info[attr] = None
            results.append(element_info)
        user_id = config.get('configurable', {}).get(
            'user_id', 'unknown') if config else 'unknown'
        logger.info(
            f"用户:[{user_id}]执行工具[Playwright 获取元素信息],URL:[{url}],选择器:[{selector}]")
        return json.dumps(results, ensure_ascii=False, indent=2)
    except Exception as ex:
        logger.error(f"获取元素信息失败: {ex}")
        return f"错误: {str(ex)}"


# 清理资源的工具
async def cleanup_playwright():
    """清理 Playwright 资源"""
    await browser_manager.close()


# 使用示例
if __name__ == "__main__":
    import sys

    async def main():
        test_config = RunnableConfig(configurable={"user_id": "test_user"})
        global PLAYWRIGHT_HEADLESS
        PLAYWRIGHT_HEADLESS = False
        print("测试获取页面内容:")
        result = await playwright_get_page_content(
            "https://httpbin.org/html", config=test_config)
        print(result[:500] + "..." if len(result) > 500 else result)
        await cleanup_playwright()
    asyncio.run(main())
